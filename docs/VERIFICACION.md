# Verificación de entrega

7 de noviembre de 2026. Navegador: Microsoft Edge (Chromium), automatizado con Playwright. Las capturas corresponden al sitio generado, con datos reales de los documentos y configuración comercial vacía.

- Páginas: 39 en total; inicio, catálogo, cotización y las 36 fichas de modelos/líneas generales.
- Anchos: 320, 390, 768, 1024 y 1440 px. Sin desbordamiento horizontal e imágenes cargadas.
- Inspección visual: portada, catálogo general y de energía, fichas de flota, torre solar, generador y línea de bombas, tablas y contacto en escritorio y móvil.
- Navegación móvil: apertura, enlaces, cierre con Escape y devolución del foco.
- Catálogo: seis categorías, 22 modelos documentados, 14 líneas generales y cuatro categorías pendientes. Búsqueda insensible a mayúsculas y tildes, filtros de tipo y procedencia, carga de todos los productos con «Mostrar más», combinación sin resultados, restablecimiento y enlaces directos. Se distingue la flota confirmada del catálogo del fabricante.
- Cotización: producto y estado comercial conservados desde las 36 fichas, validación de campos, resumen local, copia al portapapeles, descarga y ocultamiento del resumen cuando cambian los datos. Sin peticiones de envío.
- Contacto: WhatsApp, correo y dirección vacíos por indicación del usuario. Los enlaces de salida se comprobaron únicamente con configuración de prueba interceptada en el navegador; no se abrieron aplicaciones ni se enviaron mensajes. La configuración real permanece vacía.
- Apertura directa de HTML: búsqueda y traslado del modelo a cotización sin servidor.
- Revisión estática: 1316 enlaces, recursos y anclas internos correctos, sin IDs duplicados, etiquetas de plantilla pendientes ni CSS/JavaScript inline.
- PRAMAC público: tres páginas; el texto coincide con las páginas técnicas 2-4 del original. La constancia de la primera página no está incluida. PDF renderizado e inspeccionado visualmente.

El resultado detallado y el número final de comprobaciones están en `qa/resultados.json`. No se afirma entrega real de mensajes, configuración de un servidor de correo, verificación física de la flota ni publicación en hosting. Los pendientes técnicos y comerciales se detallan en `REVISION-INICIAL.md`.
