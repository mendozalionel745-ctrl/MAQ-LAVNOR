# Cobertura completa de los documentos

Actualización del 7 de noviembre de 2026 tras la petición de incorporar el listado completo. Se conserva el diseño aprobado y se amplían los datos, imágenes, fichas y opciones de consulta.

## 22 modelos identificados

| Familia | Modelos | Fuente |
| --- | --- | --- |
| PRAMAC | LSW-3Y | PDF PRAMAC, páginas técnicas 2-4 |
| HiLight solar / baterías | S2+, PS 3 | Presentaciones 6 y 14; tabla 18 |
| HiLight híbrida | BI+ 4 | Presentación 4-5; tabla 18 |
| HiLight diésel LED | H6+, B6+, V4+, V5+ | Presentaciones 7-10; tabla 18 |
| HiLight halogenuro metálico | V4, V4W | Presentación 11; tablas 18-19 |
| HiLight eléctrica LED | E3+, PE 3, V2+, V3+ | Presentaciones 13, 15-16; tabla 19 |
| Generadores | P2000i, P2500i, P3000, P3500i, P6000i, P6500, P8000 | Tabla de fuentes de alimentación, página 15 |
| Almacenamiento | ZBP2000 (también escrito ZBP 2000) | Páginas 14-15 |

Solo LSW-3Y y V5+ tienen pertenencia a flota confirmada por el usuario. El resto se publica con disponibilidad por confirmar. Cada registro tiene imagen extraída de su página, información disponible, fuente y acceso a consulta con su identificador. Las fotografías compartidas por varias columnas de generadores están expresamente rotuladas como compartidas y de resolución original reducida.

## 14 líneas generales del cuadro de página 20

Estas líneas NO son 14 modelos adicionales. El cuadro no identifica sus modelos individuales. Cada una tiene imagen, información de línea, rango original cuando existe y una página de consulta, señalando los datos pendientes.

- Almacenamiento: extra pequeño (2-10 kVA), pequeño (15-150 kVA), mediano (200-500 kVA).
- Cargador rápido: 160 kW.
- Generadores: transportables (1,6-12 kVA), especializados (9-660* kVA), versátiles (9-1250* kVA), gran potencia (800–1450 kVA).
- Bombas: eléctricas sumergibles (hasta 18 000 l/min), eléctricas centrífugas autocebantes (833–23 300 l/min), centrífugas autocebantes (833–23 300 l/min).
- Torres: diésel, batería y eléctricas; este cuadro no aporta rangos para esas tres líneas.

El asterisco de generadores remite a las múltiples configuraciones del fabricante. Los rangos de almacenamiento se mantienen en kVA, tal como aparecen; no se reinterpretan como kWh.

Las tres soluciones digitales mencionadas al final (FleetLink y dos herramientas de dimensionamiento) se reconocen como servicios/herramientas del fabricante. No se presentan como maquinaria disponible ni como funciones implementadas por MAQ Lavnor.

## Extracción y discrepancias

Las tablas se extraen por celdas con pdfplumber. Solo se extienden celdas combinadas; las celdas vacías y los guiones no se completan por inferencia. La extracción literal queda en data/fuentes-atlas-tablas.json y los valores publicados en data/catalogo.json. No se mezclan fichas de diferentes modelos.

- S2+: tabla 11 | 22 h; presentación hasta 11 h al 100%. No se asigna un régimen a cada cifra de la tabla sin confirmación.
- PS 3: la tabla clasifica la fuente como solar; el texto describe ZBP2000, paneles y alimentación externa. El asterisco de temperatura no tiene aclaración identificable en la página.
- H6+: presentación HardHat® y celda de carrocería HardBody®. Se conserva la discrepancia.
- B6+: celdas de alternador con juegos dobles de potencia/protección y correspondencia no explicada. Se conservan los valores de la celda.
- V5+: autonomía 137 | 145 h. Las 200 h de la presentación de página 10 se atribuyen a V4+, no a V5+.
- E3+: presentación hasta 100 km/h de estabilidad; tabla 80 km/h. Se muestra la tabla con observación de la discrepancia.
- PE 3: párrafo 3000 m3; recuadro y tabla 3000 m2. Se publica la unidad de tabla y se señala la errata del párrafo.
- V3+: tabla 2500 m2 a media de 10 luxes; presentación 3000 m2 con etiqueta V2+ repetida. Se conserva la tabla y se señala la ambigüedad.
- Generadores: la tabla aporta modelo y potencia en kW, pero no motor, tensión, frecuencia, combustible, dimensiones ni peso. La imagen compartida no acredita la configuración exacta de cada modelo.

Los dos documentos no contienen modelos ni fichas de minicargadores, rodillos tandem, compresoras, martillos hidráulicos/neumáticos/fragmentadores o camionetas. Sus categorías solicitadas permanecen visibles y marcadas como pendientes de documentación.

WhatsApp, correo y dirección permanecen vacíos por indicación del usuario. La consulta prepara un texto local; no envía solicitudes.
