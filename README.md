# MAQ Lavnor

Web estática de alquiler de maquinaria, en español. HTML, CSS, JavaScript e imágenes locales; no requiere Node, paquetes, CDN ni compilación para visualizarla.

## Abrir

Abrir `index.html` en el navegador o servir la carpeta con Python:

```powershell
python -m http.server 4174 --bind 127.0.0.1
```

Visitar http://127.0.0.1:4174. No se ha publicado en un hosting.

## Estructura y edición

- `index.html`: inicio.
- `catalogo.html`: catálogo y filtros.
- `equipos/`: 36 páginas individuales: 22 modelos identificados y 14 líneas generales del fabricante. Dos modelos tienen flota confirmada.
- `cotizacion.html`: consulta local con modelo o tipo preseleccionado.
- `assets/css/styles.css`: diseño y adaptación móvil.
- `assets/js/`: navegación, filtros, consulta y configuración comercial.
- `assets/images/`: fotografías extraídas de los PDF, iconos y logo original.
- `assets/documents/`: ficha PRAMAC de tres páginas técnicas y catálogo Atlas original.
- `data/catalogo.json`: marcas, modelos, categorías, especificaciones, unidades y procedencia por página.
- `data/fuentes-atlas-tablas.json`: extracción por celdas de las tablas originales de páginas 18-19.
- `templates/`: HTML fuente de las páginas y estructura compartida.
- `scripts/build_site.py`: genera las páginas HTML desde datos y plantillas; requiere solo Python estándar.
- `scripts/import_atlas_catalogue.py`: reimportación reproducible del documento Atlas con pypdf, pdfplumber y Pillow; reconstruye los registros de ese PDF y extrae sus imágenes.
- `docs/REVISION-INICIAL.md`: diagnóstico, fuentes, ambigüedades y pendientes comerciales.
- `docs/qa/`: capturas y resultados de la verificación.

Para actualizar datos o textos, editar `data/catalogo.json` o `templates/`, y ejecutar:

```powershell
python scripts/build_site.py
```

No editar el HTML generado si se desea conservar los cambios al regenerar.

## Contacto: estado real

Por indicación del cliente, WhatsApp, correo y dirección quedan vacíos. No hay endpoint, almacenamiento de solicitudes ni envío por servidor. El formulario prepara un resumen local que se puede copiar o descargar; siempre aclara que no se ha enviado. No usa cookies ni localStorage.

Para activar canales, rellenar `assets/js/config.js` con datos confirmados: WhatsApp con código de país y solo dígitos, correo válido y dirección. La página de contacto mostrará los datos y ofrecerá abrir WhatsApp o el cliente de correo con el equipo y mensaje preparados. El envío se completa en la aplicación elegida: abrir un enlace no acredita recepción. Actualizar también el rótulo de contacto del pie en `templates/layout.html` y regenerar. Si se requiere envío directo de formulario, será necesario implementar y verificar un backend, antispam y aviso de privacidad antes de presentarlo como disponible.

## Fuentes

Datos técnicos provenientes únicamente de los PDF suministrados, sin conversiones de unidades. Tras la ampliación solicitada, se incorporó toda la gama documentada: 13 modelos HiLight, 7 generadores, ZBP2000 y PRAMAC LSW-3Y. También se muestran las 14 líneas generales de la página «Catálogo de productos», identificadas como líneas sin modelos individuales, con sus rangos originales.

El usuario confirmó LSW-3Y y HiLight V5+ en flota. Los demás modelos se presentan como catálogo del fabricante con disponibilidad por confirmar. Las fichas de movimiento de tierras, aire, complementos y unidades livianas siguen pendientes: estos PDF no identifican sus modelos.

El catálogo incluye filtros por familia, tipo y procedencia (todo, flota confirmada, modelos del fabricante y líneas). Muestra inicialmente 12 productos y permite cargar los restantes. Sin JavaScript se muestran todos. El estado comercial se conserva al preparar la consulta.

La cobertura de la fuente y las discrepancias identificadas se documentan en `docs/CATALOGO-COMPLETO.md`. Algunas fotos de generadores se comparten entre columnas del documento y tienen baja resolución: las fichas lo indican.

El PDF PRAMAC suministrado incluía una primera página ajena con firmas y datos personales. Se excluyó de la descarga pública. Se conservaron únicamente las páginas técnicas 2-4, sin modificar su contenido. Las fotografías son referenciales del fabricante; confirmar la configuración de las unidades antes de ofertar.

## Verificación

`scripts/verify_site.cjs` realiza pruebas de aceptación con Playwright y Microsoft Edge: cinco anchos (320, 390, 768, 1024 y 1440 px), todas las páginas, imágenes, menú móvil, filtros, contexto de cotización, resumen, copia y descarga. También comprueba el cableado de WhatsApp/correo con configuración aislada en el navegador sin modificar producción ni enviar mensajes.

```powershell
node scripts/verify_site.cjs http://127.0.0.1:4174 RUTA_AL_MODULO_PLAYWRIGHT
```

Los datos comerciales, la disponibilidad en fechas concretas y la entrega real de mensajes no pueden verificarse mientras no se proporcionen y activen los canales.
