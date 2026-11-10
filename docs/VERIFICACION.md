# Verificación de entrega · 10 de noviembre de 2026

Selección vigente: nueve equipos. Navegador Microsoft Edge (Chromium), automatizado con Playwright. Resultado: 352 comprobaciones correctas, sin errores JavaScript ni recursos HTTP fallidos.

- Trece páginas: inicio, Nosotros, catálogo, cotización y nueve fichas individuales.
- Nosotros: navegación móvil, enlace activo, dos fotografías ampliables y revisión visual en escritorio y móvil. Accesos desde inicio, menú y pie; misión, visión, valores y razones para elegir la empresa.
- Mapa del Perú e imagen ilustrativa cargados; marcos de las dos fotos con idéntico ancho y alto en inicio y Nosotros para los cinco anchos probados. Las animaciones respetan movimiento reducido. Las capturas congelan animaciones para mostrar el estado final.
- Anchos de 320, 390, 768, 1024 y 1440 px: sin desbordamiento horizontal, imágenes cargadas y un título principal por página.
- Revisión visual de las fichas, tablas, dimensiones y fotografías de los equipos nuevos en escritorio y móvil. Bobcat y Dynapac incorporan esquemas ampliables relacionados con sus cotas.
- Inicio y catálogo con los nueve equipos visibles. Fichas, imágenes y selectores sin los 34 registros excluidos de la ampliación anterior. El importador de la gama completa ya no existe.
- Filtros por familia y tipo, búsqueda con/sin tildes, estado vacío, restablecimiento y enlaces directos. Solo generación de energía y unidades livianas carecen de modelos documentados.
- CAT 246D confirmado por el usuario; se verifica que la ficha y la consulta usen ese identificador.
- Revisión de datos clave: presiones/caudales KAESER, peso y consumo de aire TEX P60S, valores originales UG3300, potencia/capacidad CAT, capacidad/peso Bobcat y compactación Dynapac.
- Consulta preseleccionada desde las nueve fichas; validación, preparación local, copia, descarga y ocultamiento de resumen al editar. Las acciones no hacen peticiones para enviar datos; se permiten las cargas GET de recursos estáticos locales.
- Los enlaces antiguos a equipos retirados no preseleccionan una máquina inexistente.
- WhatsApp, correo y dirección reales permanecen vacíos. El cableado futuro se prueba con configuración aislada en el navegador, sin modificar producción ni enviar mensajes.
- Apertura directa de HTML: búsqueda y paso del equipo seleccionado a consulta, sin servidor.
- Comprobación estática: 514 referencias internas válidas entre enlaces, recursos y anclas; sin identificadores duplicados ni plantillas incompletas.
- Los siete PDF nuevos publicados se cotejan con sus originales. La copia de la ficha PRAMAC conserva la exclusión de la página ajena con firmas.

Capturas y detalle en qa/. La prueba de vistas por ancho no equivale a pruebas en dispositivos físicos. No se afirma entrega real de mensajes, verificación física de unidades ni publicación en hosting. Los datos pendientes de las fuentes se identifican en ALCANCE-CATALOGO.md y en las propias fichas.
