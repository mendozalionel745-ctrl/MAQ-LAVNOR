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
- `nosotros.html`: presentación, misión, visión, valores y galería de entregas; propuesta editorial descrita en `docs/NOSOTROS.md`.
- `catalogo.html`: catálogo y filtros.
- `equipos/`: nueve fichas, limitadas a la selección aprobada el 10/11/2026.
- `cotizacion.html`: consulta local con modelo o tipo preseleccionado.
- `assets/css/styles.css`: diseño y adaptación móvil.
- `assets/js/`: navegación, filtros, consulta y configuración comercial.
- `assets/images/`: fotografías de los PDF, imágenes adjuntas del cliente, esquemas de dimensiones, iconos y logo original.
- `assets/documents/`: documentos técnicos suministrados. El folleto Atlas de iluminación se referencia únicamente para V5+.
- `data/catalogo.json`: marcas, modelos, categorías, especificaciones, unidades y procedencia por página.
- `templates/`: HTML fuente de las páginas y estructura compartida.
- `scripts/build_site.py`: genera las páginas HTML desde datos y plantillas; requiere solo Python estándar.
- `scripts/import_fleet.py`: importa exclusivamente la selección de nueve equipos desde los documentos e imágenes originales en Downloads. Requiere pypdf y Pillow solo para reimportar; no son dependencias de la web. Se retiró el importador de la gama completa para evitar que se reincorporen equipos excluidos.
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

El 10/11/2026 el usuario corrigió el alcance y solicitó retirar la ampliación anterior. La selección vigente es: PRAMAC LSW-3Y, Atlas Copco HiLight V5+, KAESER M100 y M235, Atlas Copco TEX P60S, HYDROKHAN UG3300, CAT 246D, Bobcat S650 y Dynapac DTR75. CAT 246D fue confirmado expresamente: el nombre del archivo decía 243D, pero sus páginas describen 246D.

Los 34 registros adicionales de la gama anterior se retiraron del catálogo, las fichas, las imágenes y los selectores de consulta. No se incorporan otros modelos, herramientas o implementos por aparecer en un folleto.

El catálogo muestra los nueve equipos sin paginación y permite filtrar por categoría y tipo, o buscar por marca/modelo. Se conservan las seis categorías originales; generación de energía y unidades livianas siguen sin modelos documentados. DTR75 se identifica como rodillo dúplex, según su ficha. Martillos fragmentadores permanece como tipo sin modelo agregado.

Las características básicas, opciones y ambigüedades se separan en cada ficha. Se conservaron las unidades originales sin calcular equivalencias o autonomías no documentadas. Los esquemas de Bobcat y Dynapac permiten relacionar las cotas con sus tablas. La selección y los datos por revisar se documentan en `docs/ALCANCE-CATALOGO.md`.

El PDF PRAMAC suministrado incluía una primera página ajena con firmas y datos personales. Se excluyó de la descarga pública. Se conservaron únicamente las páginas técnicas 2-4, sin modificar su contenido. Las fotografías son referenciales del fabricante; confirmar la configuración de las unidades antes de ofertar.

## Verificación

`scripts/verify_site.cjs` realiza pruebas de aceptación con Playwright y Microsoft Edge: cinco anchos (320, 390, 768, 1024 y 1440 px), todas las páginas, imágenes, menú móvil, filtros, contexto de cotización, resumen, copia y descarga. También comprueba el cableado de WhatsApp/correo con configuración aislada en el navegador sin modificar producción ni enviar mensajes.

```powershell
node scripts/verify_site.cjs http://127.0.0.1:4174 RUTA_AL_MODULO_PLAYWRIGHT
```

Los datos comerciales, la disponibilidad en fechas concretas y la entrega real de mensajes no pueden verificarse mientras no se proporcionen y activen los canales.
