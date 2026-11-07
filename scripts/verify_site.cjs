/* Pruebas de aceptación del sitio servido. No envía consultas ni abre contactos externos.
   node scripts/verify_site.cjs http://127.0.0.1:4174 [ruta al módulo playwright] */
const { chromium } = require(process.argv[3] || 'playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const base = process.argv[2] || 'http://127.0.0.1:4174';
const qa = path.join(__dirname, '../docs/qa');
fs.mkdirSync(qa, { recursive: true });
const data = JSON.parse(fs.readFileSync(path.join(__dirname, '../data/catalogo.json'), 'utf8'));
const allItems = [...data.equipment, ...(data.productLines || [])];
const pendingFamilies = data.categories.filter(category => !allItems.some(item => item.category === category.id));
const screenshotPages = new Set(['index.html', 'catalogo.html', 'cotizacion.html',
  'equipos/pramac-lsw-3y.html', 'equipos/atlas-copco-hilight-v5.html',
  'equipos/atlas-copco-hilight-s2.html', 'equipos/atlas-copco-p3000.html',
  'equipos/atlas-copco-linea-bombas-sumergibles.html']);

(async () => {
  const browser = await chromium.launch({ headless: true, channel: 'msedge' });
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, permissions: ['clipboard-read', 'clipboard-write'] });
  const page = await context.newPage();
  const errors = [];
  const failed = [];
  const checks = [];
  page.on('pageerror', error => errors.push(error.message));
  page.on('response', response => { if (response.status() >= 400) failed.push(`${response.status()} ${response.url()}`); });
  const check = (name, condition) => { assert.ok(condition, name); checks.push(name); };
  try {
    const pages = ['index.html', 'catalogo.html', ...allItems.map(item => `equipos/${item.id}.html`), 'cotizacion.html'];
    for (const width of [1440, 1024, 768, 390, 320]) {
      await page.setViewportSize({ width, height: width < 600 ? 844 : 1000 });
      for (const item of pages) {
        const response = await page.goto(`${base}/${item}`);
        await page.evaluate(async () => {
          const images = [...document.images];
          images.forEach(image => { image.loading = 'eager'; });
          await Promise.all(images.map(image => image.decode().catch(() => {})));
        });
        check(`HTTP 200 · ${item} · ${width}px`, response.status() === 200);
        check(`Sin desbordamiento · ${item} · ${width}px`, await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
        check(`Imágenes cargadas · ${item} · ${width}px`, await page.evaluate(() => [...document.images].every(i => i.complete && i.naturalWidth > 0)));
        check(`Un título principal · ${item}`, await page.locator('h1').count() === 1);
        if ([1440, 390].includes(width) && screenshotPages.has(item)) {
          const name = item.replace('equipos/', '').replace('.html', '');
          await page.screenshot({ path: path.join(qa, `${name}-${width}.png`), fullPage: true });
          if (item === 'index.html') await page.screenshot({ path: path.join(qa, `portada-${width}.png`) });
        }
      }
    }
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto(`${base}/index.html`);
    const menu = page.locator('.menu-toggle');
    await menu.click();
    check('Menú móvil abre', await menu.getAttribute('aria-expanded') === 'true');
    await page.keyboard.press('Escape');
    check('Escape cierra menú y devuelve foco', await menu.getAttribute('aria-expanded') === 'false' && await menu.evaluate(el => el === document.activeElement));
    await menu.click();
    await page.locator('#main-navigation a[href="catalogo.html"]').click();
    check('Menú móvil navega al catálogo', page.url().endsWith('/catalogo.html'));
    await page.setViewportSize({ width: 1440, height: 1000 });

    await page.goto(`${base}/catalogo.html`);
    check('Todos los modelos y líneas están en catálogo', await page.locator('.equipment-card').count() === allItems.length);
    check('Primera página de doce productos', await page.locator('.equipment-card:visible').count() === Math.min(12, allItems.length));
    check('Familias pendientes correctas', await page.locator('.pending-family:visible').count() === pendingFamilies.length);
    while (await page.locator('#load-more').isVisible()) await page.locator('#load-more').click();
    check('Mostrar más permite ver todos los productos', await page.locator('.equipment-card:visible').count() === allItems.length);
    const categories = await page.locator('[data-filter]').evaluateAll(items => items.map(i => i.dataset.filter));
    for (const category of categories) {
      await page.locator(`[data-filter="${category}"]`).click();
      const visible = await page.locator('.equipment-card:visible,.pending-family:visible').evaluateAll(items => items.map(i => i.dataset.category));
      check(`Filtro de familia · ${category}`, category === 'todos' ? visible.length === Math.min(12, allItems.length) + pendingFamilies.length : visible.length > 0 && visible.every(id => id === category));
    }
    await page.locator('#clear-filters').click();
    await page.locator('#search').fill('iluminacion');
    check('Búsqueda ignora tildes', await page.locator('.equipment-card:visible').count() > 2);
    await page.locator('#search').fill('PRAMAC');
    check('Búsqueda por marca', await page.locator('.equipment-card:visible').count() === 1);
    await page.locator('#equipment-type').selectOption('Compresoras');
    check('Combinación sin coincidencias muestra estado vacío', await page.locator('#no-results').isVisible());
    await page.locator('#clear-filters').click();
    check('Limpiar restablece resultados', await page.locator('.equipment-card:visible').count() === Math.min(12, allItems.length) && await page.locator('#search').inputValue() === '');
    await page.goto(`${base}/catalogo.html?categoria=complementos&tipo=Martillos%20hidr%C3%A1ulicos`);
    check('Enlace directo de familia y tipo', await page.locator('.pending-family:visible').count() === 1 && await page.locator('.equipment-card:visible').count() === 0);
    await page.goto(`${base}/catalogo.html?categoria=inventada&tipo=inventado`);
    check('Filtros desconocidos usan catálogo completo', await page.locator('.equipment-card:visible').count() === Math.min(12, allItems.length));
    await page.locator('#catalog-source').selectOption('confirmed');
    check('Flota confirmada contiene solo los dos modelos autorizados', await page.locator('.equipment-card:visible').count() === 2 && await page.locator('.equipment-card:visible').evaluateAll(items => items.every(item => item.dataset.confirmed === 'true')));
    await page.locator('#catalog-source').selectOption('manufacturer');
    while (await page.locator('#load-more').isVisible()) await page.locator('#load-more').click();
    check('Modelos del fabricante separados de la flota', await page.locator('.equipment-card:visible').count() === data.equipment.filter(item => !item.confirmed).length);
    await page.locator('#catalog-source').selectOption('lines');
    while (await page.locator('#load-more').isVisible()) await page.locator('#load-more').click();
    check('Las catorce líneas generales tienen imagen y ficha propia', await page.locator('.equipment-card:visible').count() === data.productLines.length);
    await page.goto(`${base}/catalogo.html?categoria=generacion-de-energia`);
    check('Generadores y almacenamiento tienen resultados', await page.locator('.equipment-card:visible').count() > 0);
    await page.screenshot({ path: path.join(qa, 'catalogo-energia-1440.png'), fullPage: true });
    await page.goto(`${base}/catalogo.html?tipo=Bombas%20de%20achique&origen=lines`);
    check('Tres líneas de bombas documentadas', await page.locator('.equipment-card:visible').count() === 3);

    for (const item of allItems) {
      await page.goto(`${base}/equipos/${item.id}.html`);
      check(`Ficha individual correcta · ${item.id}`, await page.locator('h1').textContent() === item.model);
      check(`Estado comercial correcto · ${item.id}`, (await page.locator('.availability').textContent()).includes(item.confirmed ? 'Flota confirmada' : 'por confirmar'));
      await page.locator('.detail-copy .button').click();
      check(`Consulta identifica producto · ${item.id}`, await page.locator('#equipment').inputValue() === item.id);
      if (!item.confirmed) check(`Consulta señala estado pendiente · ${item.id}`, (await page.locator('.selection-state').textContent()).includes(item.kind === 'line' ? 'modelos por definir' : 'por confirmar'));
    }

    for (const [id, name] of [['pramac-lsw-3y', 'PRAMAC LSW-3Y'], ['atlas-copco-hilight-v5', 'ATLAS COPCO HiLight V5+']]) {
      await page.goto(`${base}/equipos/${id}.html`);
      await page.locator('.detail-copy .button').click();
      check(`Cotización conserva modelo · ${id}`, await page.locator('#equipment').inputValue() === id && await page.locator('#selected-equipment').textContent() === name);
    }
    const before = [];
    page.on('request', request => before.push(request.url()));
    await page.locator('#prepare-quote').click();
    check('Formulario incompleto no prepara resumen', !await page.locator('#quote-result').isVisible());
    await page.locator('[name=name]').fill('Prueba de revisión');
    await page.locator('[name=company]').fill('Empresa de prueba');
    await page.locator('[name=email]').fill('revision@example.com');
    await page.locator('[name=location]').fill('Lima');
    await page.locator('[name=period]').fill('15 días');
    await page.locator('[name=details]').fill('Dos unidades. Prueba local sin envío.');
    await page.locator('#prepare-quote').click();
    check('Resumen conserva modelo y requerimiento', (await page.locator('#quote-message').inputValue()).includes('ATLAS COPCO HiLight V5+') && (await page.locator('#quote-message').inputValue()).includes('Dos unidades'));
    check('Explicación de no envío visible', (await page.locator('#result-state').textContent()).includes('No se ha enviado'));
    check('No existen canales de envío activos', !await page.locator('#send-whatsapp').isVisible() && !await page.locator('#send-email').isVisible());
    await page.locator('#copy-quote').click();
    check('Copiar conserva el equipo', (await page.evaluate(() => navigator.clipboard.readText())).includes('ATLAS COPCO HiLight V5+'));
    const downloadPromise = page.waitForEvent('download');
    await page.locator('#download-quote').click();
    const download = await downloadPromise;
    const downloaded = await download.path();
    check('Descarga texto con modelo', fs.readFileSync(downloaded, 'utf8').includes('ATLAS COPCO HiLight V5+'));
    check('Preparación sin peticiones de envío', before.every(url => url.startsWith('blob:')));
    await page.locator('[name=period]').fill('30 días');
    check('Modificar datos oculta resumen desactualizado', !await page.locator('#quote-result').isVisible());

    // Se comprueba el cableado futuro con configuración aislada, sin modificar los archivos.
    await page.route('**/assets/js/config.js', route => route.fulfill({ contentType: 'text/javascript', body: 'window.MAQ_CONFIG={whatsapp:"51987654321",email:"revision@example.com",address:"Dirección de prueba"};' }));
    await page.reload();
    await page.locator('[name=name]').fill('Prueba');
    await page.locator('[name=location]').fill('Lima');
    await page.locator('[name=period]').fill('15 días');
    await page.locator('#prepare-quote').click();
    const wa = new URL(await page.locator('#send-whatsapp').getAttribute('href'));
    check('WhatsApp configurado conserva modelo y mensaje', wa.hostname === 'wa.me' && wa.searchParams.get('text').includes('ATLAS COPCO HiLight V5+'));
    const mail = await page.locator('#send-email').getAttribute('href');
    check('Correo configurado conserva modelo', decodeURIComponent(mail).includes('ATLAS COPCO HiLight V5+'));
    await page.unroute('**/assets/js/config.js');
    await page.reload();
    check('Configuración real continúa vacía', await page.locator('[data-contact=whatsapp]').textContent() === 'Pendiente de completar');
    await page.goto(pathToFileURL(path.join(__dirname, '../catalogo.html')).href);
    await page.locator('#search').fill('PRAMAC');
    check('Catálogo funciona al abrir HTML local', await page.locator('.equipment-card:visible').count() === 1);
    await page.locator('.equipment-card:visible .small-quote').click();
    check('HTML local conserva equipo en consulta', await page.locator('#equipment').inputValue() === 'pramac-lsw-3y');
    check('Sin errores JavaScript', errors.length === 0);
    check('Sin recursos HTTP fallidos', failed.length === 0);
    fs.writeFileSync(path.join(qa, 'resultados.json'), JSON.stringify({ date: '2026-11-07', browser: 'Microsoft Edge / Chromium', checks: checks.length, passed: checks, errors, failed, productionContact: 'Pendiente por indicación del usuario. Sin envío por servidor.' }, null, 2));
    console.log(`${checks.length} comprobaciones correctas. Sin errores JavaScript ni recursos fallidos.`);
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
