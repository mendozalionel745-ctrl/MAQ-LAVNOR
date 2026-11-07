# Revisión del proyecto y fuentes

> Registro histórico de la primera revisión. La selección inicial de solo dos modelos fue ampliada a petición del usuario: el estado actual contiene 22 modelos documentados y 14 líneas generales, todos con imagen y página propia. Véase CATALOGO-COMPLETO.md. La disponibilidad de los modelos adicionales no se da por confirmada.

## Estado inicial, antes de modificar

El repositorio contenía index.html (estructura, Tailwind CDN, CSS y JavaScript en un solo archivo) y assets/maqlogo.jpg. Sin herramientas de compilación, dependencias instaladas ni backend. Se conserva la implementación con HTML, CSS y JavaScript, la identidad negra y amarilla, el logo y las seis familias solicitadas.

Problemas: portada dominada por el logo; tarjetas sin navegación; ausencia de fotografías y páginas técnicas; cotización que conserva solo la categoría; teléfono de ejemplo; correo y dirección sin verificar; enlaces sociales vacíos; formulario que muestra recepción exitosa sin envío; afirmaciones 24/7, respuesta en 24 horas y caso de operación no respaldados para MAQ Lavnor.

## Referencia de organización

Se revisaron https://mecorp.com.pe/ y https://mecorp.com.pe/torres-de-iluminacion/ el 7 de noviembre de 2026. Patrones útiles: navegación por familias/subfamilias, acceso al catálogo desde la portada, ficha con fotografía y datos principales, acceso repetido a cotización. Se crea composición, textos y código propios. No se reutilizan su identidad, contactos, fotografías ni datos técnicos.

## Fuentes y trazabilidad

- FT_Luminaria_PRAMAC_LSW3.pdf: 4 páginas. La primera es una constancia de un tercero con firmas y datos personales, sin especificaciones. NO se publica ni se usa para afirmar experiencia o clientes de MAQ Lavnor. Páginas 2-4: ficha LSW-3Y [LED], impresa el 13/05/2022. La descarga pública contiene solo esas tres páginas.
- FT_Luminaria_ATLAS COPCO_Hilight V5+.pdf: catálogo de fabricante de 20 páginas, edición 2023. Se extrae exclusivamente HiLight V5+ de páginas 10 y 18. Los demás modelos mencionados no se incorporan a la flota. Descarga rotulada como catálogo del fabricante, no como inventario.
- Fotografías de producto: PRAMAC página 2; V5+ imagen derecha de página 10. Fotografía ambiental: portada del catálogo Atlas, rotulada como referencia del fabricante; muestra varios equipos y NO acredita composición de la flota.

El usuario confirmó que LSW-3Y y HiLight V5+ pertenecen a la flota. La disponibilidad para fechas concretas se consulta. Solicitó dejar teléfono, correo y dirección sin completar.

## Datos pendientes / ambiguos

1. Datos comerciales: WhatsApp, correo, dirección, razón social/RUC, cobertura, tarifas, condiciones de transporte/alquiler, tiempos de respuesta, prestaciones de soporte y política de privacidad. No se inventan.
2. Modelos, fotografías y fichas de minicargadores, rodillos tandem, grupos electrógenos, compresoras, martillos hidráulicos, neumáticos, fragmentadores y camionetas. Las familias se muestran con marcador de información técnica pendiente; no se crean modelos ficticios.
3. PRAMAC: el nombre de archivo dice LSW3, la ficha identifica LSW-3Y [LED]. Se utiliza el identificador de la ficha. La potencia de lámparas se publica TOTAL (1280 W), sin inferir potencia por foco.
4. PRAMAC: resistencia al viento impresa como `80 (con carácter inicial extraño), unidad Km/h. Se conserva el valor y se señala para revisión. Potencia del alternador titulada literalmente Continuous power 125°/40°: verificar significado de las condiciones. Ficha: 240 V; enchufe: 230V 16A IP44. No se equiparan estos valores ni se corrigen sin confirmar.
5. Atlas: la tabla p.18 presenta 50 | 60 Hz y valores dobles asociados. Se mantienen las alternativas y unidades originales; confirmar configuración de la unidad en flota antes de ofertar. Autonomía V5+: 137 | 145 h; no atribuir las 200 h de V4+ a V5+.
6. Atlas: consumo de 0,7 l/h en p.10; condiciones de medición no detalladas en esa página. No se garantiza rendimiento real en obra. Fotografías de fabricante referenciales.

## Secuencia realizada

1. Auditoría, extracción de textos e inspección visual de páginas técnicas, datos en data/catalogo.json y fotografías locales.
2. Inicio propio, CSS adaptable y navegación accesible; comprobación visual de escritorio y celular.
3. Catálogo con seis familias, filtros por familia/tipo/búsqueda, dos fichas técnicas y documentos descargables.
4. Consulta con equipo identificado, resumen local copiable/descargable y canales explícitamente pendientes. Sin recepción ficticia, sin almacenamiento de datos personales ni envío por servidor.
