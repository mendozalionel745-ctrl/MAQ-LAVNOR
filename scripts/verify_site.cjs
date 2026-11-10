/* Verificación de aceptación. Prepara consultas de prueba, nunca las envía.
   node scripts/verify_site.cjs http://127.0.0.1:4174 [módulo playwright] */
const { chromium } = require(process.argv[3] || 'playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const root = path.join(__dirname, '..');
const base = process.argv[2] || 'http://127.0.0.1:4174';
const qa = path.join(root, 'docs/qa');
const data = JSON.parse(fs.readFileSync(path.join(root, 'data/catalogo.json'), 'utf8'));
const approvedIds = ['pramac-lsw-3y', 'atlas-copco-hilight-v5', 'kaeser-m100', 'kaeser-m235',
  'atlas-copco-tex-p60s', 'hydrokhan-ug3300', 'cat-246d', 'bobcat-s650', 'dynapac-dtr75'];
const pending = data.categories.filter(category => !data.equipment.some(item => item.category === category.id));
const checks = [];
function check(name, condition) { assert.ok(condition, name); checks.push(name); }

(async () => {
  check('Datos limitados a los nueve equipos aprobados', data.equipment.length === 9 && data.equipment.every(item => approvedIds.includes(item.id)));
  check('Sin líneas generales del fabricante', !data.productLines?.length);
  const htmlFiles = fs.readdirSync(path.join(root, 'equipos')).filter(file => file.endsWith('.html'));
  check('No quedan fichas HTML de equipos retirados', htmlFiles.length === 9 && htmlFiles.every(file => approvedIds.includes(file.replace('.html', ''))));
  check('Modelo CAT confirmado como 246D', data.equipment.find(item => item.id === 'cat-246d').model === '246D');
  const browser = await chromium.launch({ headless: true, channel: 'msedge' });
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, permissions: ['clipboard-read', 'clipboard-write'] });
  const page = await context.newPage();
  const errors = [];
  const failed = [];
  page.on('pageerror', error => errors.push(error.message));
  page.on('response', response => { if (response.status() >= 400) failed.push(`${response.status()} ${response.url()}`); });
  fs.mkdirSync(qa, { recursive: true });
  try {
    const pages = ['index.html', 'nosotros.html', 'catalogo.html', ...approvedIds.map(id => `equipos/${id}.html`), 'cotizacion.html'];
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
        check(`Imágenes cargadas · ${item} · ${width}px`, await page.evaluate(() => [...document.images].every(image => image.complete && image.naturalWidth > 0)));
        check(`Un título principal · ${item} · ${width}px`, await page.locator('h1').count() === 1);
        if (['index.html', 'nosotros.html'].includes(item)) {
          const selector = item === 'nosotros.html' ? '.delivery-gallery figure>a' : '.delivery-preview a';
          const sizes = await page.locator(selector).evaluateAll(items => items.map(el => ({w:el.getBoundingClientRect().width,h:el.getBoundingClientRect().height})));
          check(`Fotografías con marcos iguales · ${item} · ${width}px`, sizes.length === 2 && Math.abs(sizes[0].w-sizes[1].w)<1 && Math.abs(sizes[0].h-sizes[1].h)<1);
        }
        if ([1440, 390].includes(width)) {
          const name = item.replace('equipos/', '').replace('.html', '');
          await page.screenshot({ path: path.join(qa, `${name}-${width}.png`), fullPage: true, animations: 'disabled' });
          if (item === 'index.html') await page.screenshot({ path: path.join(qa, `portada-${width}.png`), animations: 'disabled' });
        }
      }
    }
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto(`${base}/index.html`);
    check('Los nueve equipos aparecen también en el inicio', await page.locator('.featured-grid .equipment-card').count() === 9);
    const menu = page.locator('.menu-toggle');
    await menu.click();
    check('Menú móvil abre', await menu.getAttribute('aria-expanded') === 'true');
    await page.keyboard.press('Escape');
    check('Escape cierra menú y devuelve foco', await menu.getAttribute('aria-expanded') === 'false' && await menu.evaluate(el => el === document.activeElement));
    await menu.click();
    await page.locator('#main-navigation a[href="nosotros.html"]').click();
    check('Menú móvil navega a Nosotros', page.url().endsWith('/nosotros.html'));
    check('Nosotros tiene enlace activo', await page.locator('#main-navigation a[aria-current="page"]').textContent() === 'Nosotros');
    check('Dos fotografías de entregas ampliables', await page.locator('.delivery-gallery figure a[target="_blank"] img').count() === 2);
    check('Mapa del Perú e imagen ilustrativa cargados', await page.locator('.peru-map,.company-editorial img').evaluateAll(items => items.length === 2 && items.every(img => img.complete && img.naturalWidth > 0)));
    await page.emulateMedia({reducedMotion:'reduce'});
    check('Movimiento reducido respeta preferencias', await page.locator('.reveal').evaluateAll(items => items.every(el => getComputedStyle(el).animationName === 'none')));
    await page.emulateMedia({reducedMotion:'no-preference'});
    await page.goto(`${base}/index.html`);
    await menu.click();
    await page.locator('#main-navigation a[href="catalogo.html"]').click();
    check('Menú móvil navega al catálogo', page.url().endsWith('/catalogo.html'));
    await page.setViewportSize({ width: 1440, height: 1000 });
    check('Nueve tarjetas, sin modelos adicionales', await page.locator('.equipment-card').count() === 9);
    check('Todos los equipos están visibles sin paginación', await page.locator('.equipment-card:visible').count() === 9);
    check('Solo dos familias sin fichas', await page.locator('.pending-family:visible').count() === pending.length && pending.length === 2);
    for (const category of data.categories) {
      await page.locator(`[data-filter="${category.id}"]`).click();
      const visible = await page.locator('.equipment-card:visible,.pending-family:visible').evaluateAll(items => items.map(item => item.dataset.category));
      check(`Filtro de familia · ${category.id}`, visible.length > 0 && visible.every(id => id === category.id));
    }
    await page.locator('#clear-filters').click();
    await page.locator('#search').fill('iluminacion');
    check('Búsqueda ignora tildes', await page.locator('.equipment-card:visible').count() === 2);
    await page.locator('#search').fill('KAESER');
    check('Dos compresoras por marca', await page.locator('.equipment-card:visible').count() === 2);
    await page.locator('#equipment-type').selectOption('Minicargadores');
    check('Filtros incompatibles muestran estado vacío', await page.locator('#no-results').isVisible());
    await page.locator('#clear-filters').click();
    check('Limpiar restablece catálogo', await page.locator('.equipment-card:visible').count() === 9);
    await page.goto(`${base}/catalogo.html?categoria=complementos&tipo=Martillos%20hidr%C3%A1ulicos`);
    check('Enlace directo selecciona martillo hidráulico', await page.locator('.equipment-card:visible h3').textContent() === 'UG3300↗');
    await page.goto(`${base}/catalogo.html?categoria=inventada&tipo=inventado`);
    check('Filtros desconocidos usan catálogo completo', await page.locator('.equipment-card:visible').count() === 9);
    for (const retired of ['P2000i', 'ZBP2000', 'HiLight S2+', 'bombas de achique']) {
      await page.locator('#search').fill(retired);
      check(`Equipo retirado no aparece en búsquedas · ${retired}`, await page.locator('.equipment-card:visible').count() === 0);
    }
    const expectedDetails = {
      'kaeser-m100': ['375 cfm', '100 psig', '40 gal.'],
      'kaeser-m235': ['825 cfm', '125 psig', '119 gal.'],
      'atlas-copco-tex-p60s': ['33 kg (73 lb)', '36 l/s (76 cfm)', '8461 0227 22'],
      'hydrokhan-ug3300': ['13558 joules', '29 - 38 Ton', '250 ~ 600 bpm'],
      'cat-246d': ['55,4 kW / 74,3 hp', '975 kg / 2.150 lb', '3.368 kg / 7.424 lb'],
      'bobcat-s650': ['1253 kg', '87.10 L/min', '3657 kg'],
      'dynapac-dtr75': ['757 kg', '22 kN', '1,3 l']
    };
    for (const item of data.equipment) {
      await page.goto(`${base}/equipos/${item.id}.html`);
      check(`Ficha individual correcta · ${item.id}`, await page.locator('h1').textContent() === item.model);
      const text = await page.locator('.specs-tables').textContent();
      if (expectedDetails[item.id]) check(`Datos técnicos correctos · ${item.id}`, expectedDetails[item.id].every(value => text.includes(value)));
      await page.locator('.detail-copy .button').click();
      check(`Consulta identifica modelo · ${item.id}`, await page.locator('#equipment').inputValue() === item.id && await page.locator('#selected-equipment').textContent() === `${item.brand} ${item.model}`);
      const options = await page.locator('#equipment optgroup:first-of-type option').evaluateAll(items => items.map(item => item.value));
      check(`Selector solo contiene los nueve equipos · ${item.id}`, options.length === 9 && options.every(id => approvedIds.includes(id)));
    }
    await page.goto(`${base}/cotizacion.html?equipo=atlas-copco-p3000`);
    check('Enlace antiguo no selecciona una máquina retirada', await page.locator('#equipment').inputValue() === 'general');
    await page.goto(`${base}/cotizacion.html?equipo=atlas-copco-hilight-v5`);
    const requests = [];
    page.on('request', request => requests.push({ url: request.url(), method: request.method(), body: request.postData() }));
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
    check('No hay canales de envío activos', !await page.locator('#send-whatsapp').isVisible() && !await page.locator('#send-email').isVisible());
    await page.locator('#copy-quote').click();
    check('Copiar conserva el modelo', (await page.evaluate(() => navigator.clipboard.readText())).includes('ATLAS COPCO HiLight V5+'));
    const downloadPromise = page.waitForEvent('download');
    await page.locator('#download-quote').click();
    const download = await downloadPromise;
    check('Descarga texto con modelo', fs.readFileSync(await download.path(), 'utf8').includes('ATLAS COPCO HiLight V5+'));
    check('Preparar, copiar y descargar no envían datos', requests.every(request => request.url.startsWith('blob:') ||
      (request.method === 'GET' && !request.body && new URL(request.url).origin === new URL(base).origin && new URL(request.url).pathname.startsWith('/assets/'))));
    await page.locator('[name=period]').fill('30 días');
    check('Editar oculta el resumen desactualizado', !await page.locator('#quote-result').isVisible());
    await page.route('**/assets/js/config.js', route => route.fulfill({ contentType: 'text/javascript', body: 'window.MAQ_CONFIG={whatsapp:"51987654321",email:"revision@example.com",address:"Dirección de prueba"};' }));
    await page.reload();
    await page.locator('[name=name]').fill('Prueba');
    await page.locator('[name=location]').fill('Lima');
    await page.locator('[name=period]').fill('15 días');
    await page.locator('#prepare-quote').click();
    const wa = new URL(await page.locator('#send-whatsapp').getAttribute('href'));
    check('WhatsApp de prueba conserva modelo y mensaje', wa.hostname === 'wa.me' && wa.searchParams.get('text').includes('ATLAS COPCO HiLight V5+'));
    check('Correo de prueba conserva modelo', decodeURIComponent(await page.locator('#send-email').getAttribute('href')).includes('ATLAS COPCO HiLight V5+'));
    await page.unroute('**/assets/js/config.js');
    await page.reload();
    check('Configuración comercial real sigue vacía', await page.locator('[data-contact=whatsapp]').textContent() === 'Pendiente de completar');
    await page.goto(pathToFileURL(path.join(root, 'catalogo.html')).href);
    await page.locator('#search').fill('Bobcat');
    check('Catálogo funciona abriendo HTML local', await page.locator('.equipment-card:visible').count() === 1);
    await page.locator('.equipment-card:visible .small-quote').click();
    check('HTML local conserva equipo en consulta', await page.locator('#equipment').inputValue() === 'bobcat-s650');
    check('Sin errores JavaScript', errors.length === 0);
    check('Sin recursos HTTP fallidos', failed.length === 0);
    fs.writeFileSync(path.join(qa, 'resultados.json'), JSON.stringify({ date: '2026-11-10', browser: 'Microsoft Edge / Chromium', checks: checks.length, passed: checks, errors, failed, productionContact: 'Pendiente por indicación del usuario. Sin envío por servidor.' }, null, 2));
    console.log(`${checks.length} comprobaciones correctas. Sin errores JavaScript ni recursos fallidos.`);
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
