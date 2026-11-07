"""Importa la gama completa del PDF suministrado (pypdf, pdfplumber y Pillow).

Las tablas de páginas 18-19 se leen por celdas, sin convertir unidades.
Las líneas generales de página 20 se distinguen de los modelos identificados.
"""
from pathlib import Path
from copy import deepcopy
import json
import re

import pdfplumber
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / 'assets/documents/atlas-copco-gama-hilight.pdf'
SOURCE = 'FT_Luminaria_ATLAS COPCO_Hilight V5+.pdf'
data = json.loads((ROOT / 'data/catalogo.json').read_text(encoding='utf-8'))
reader = PdfReader(FILE)
tables_pdf = pdfplumber.open(FILE)
tables = {number: tables_pdf.pages[number - 1].extract_table() for number in (18, 19)}


def clean(value):
    return re.sub(r'\s+', ' ', value or '').strip()


def asset(identifier, page, index):
    image = reader.pages[page - 1].images[index].image
    # Conservar el canal alfa de las fotografías recortadas del fabricante.
    image = image.convert('RGBA' if 'A' in image.getbands() else 'RGB')
    destination = ROOT / f'assets/images/equipos/{identifier}.webp'
    image.save(destination, 'WEBP', quality=94)
    return dict(image=destination.relative_to(ROOT).as_posix(), imageWidth=image.width,
                imageHeight=image.height, imageSource={'page': page, 'index': index},
                lowResolution=image.width < 200)


def base_item(identifier, model, category, equipment_type, description, image_page, image_index, pages, kind='model'):
    return dict(id=identifier, brand='ATLAS COPCO', model=model, sourceModel=model if kind == 'model' else None,
                category=category, type=equipment_type, typeLabel=equipment_type,
                kind=kind, confirmed=False, description=description,
                document=f'assets/documents/atlas-copco-gama-hilight.pdf#page={pages[0]}',
                documentLabel='Ver documento del fabricante',
                documentNote='Catálogo HiLight · páginas ' + ', '.join(map(str, pages)) + ' · 2023',
                source=SOURCE, sourcePages=pages, sourceDate='2023',
                imageCaption='Fotografía referencial del catálogo del fabricante.',
                notes=['Modelo del catálogo del fabricante. Disponibilidad en MAQ Lavnor por confirmar.',
                       'Datos de la edición 2023. Confirmar la configuración, tarifa, traslado y disponibilidad antes de contratar.'],
                groups=[], **asset(identifier, image_page, image_index))


def extract_groups(page, column):
    table = tables[page]
    start = 2 if page == 18 else 3
    result = [{'title': 'Iluminación y configuración', 'page': page, 'rows': []}]
    for position, row in enumerate(table[start:], start):
        label = clean(row[0])
        if position >= start + 4 and row[1] is None:
            result.append({'title': label, 'page': page, 'rows': []})
            continue
        value = row[column]
        # Solo propagar celdas realmente combinadas, nunca celdas vacías.
        if value is None:
            for previous in range(column - 1, 1, -1):
                if row[previous] is not None:
                    value = row[previous]
                    break
        if not clean(value) or clean(value) == '-':
            continue
        unit = clean(row[1])
        if label.startswith('Cobertura lumínica'):
            label, unit = 'Cobertura lumínica', 'm2'
        # El rango de tensión ya incluye V en la celda del original.
        if label == 'Tensión nominal' and clean(value) == '100-277 V':
            unit = ''
        result[-1]['rows'].append([label, clean(value), unit])
    return [group for group in result if group['rows']]


def extra(item, page, rows):
    item['groups'].append({'title': 'Prestaciones descritas por el fabricante', 'page': page, 'rows': rows})


existing = {item['id']: deepcopy(item) for item in data['equipment']}
confirmed = [existing['pramac-lsw-3y'], existing['atlas-copco-hilight-v5']]
for item in confirmed:
    item.update(kind='model', confirmed=True, typeLabel='Torre de iluminación LED', cardTag='ILUMINACIÓN LED',
                imageCaption='Fotografía referencial del fabricante.')
confirmed[1]['notes'] = [note for note in confirmed[1]['notes'] if 'no se incorporan al inventario' not in note]
fleet_note = 'La flota confirmada se distingue del resto de la gama del fabricante, cuya disponibilidad requiere consulta.'
if fleet_note not in confirmed[1]['notes']:
    confirmed[1]['notes'].append(fleet_note)

specifications = [
    ('s2', 'HiLight S2+', 18, 2, 6, 2, 'SOLAR · LED', 'Torre LED solar con paneles extensibles, baterías y mástil manual. El fabricante indica 2000 m2 de cobertura con una media de 20 luxes.'),
    ('ps-3', 'HiLight PS 3', 18, 3, 14, 0, 'BATERÍAS / SOLAR · LED', 'Torre LED diseñada para recibir alimentación del sistema ZBP2000, con carro y dos paneles solares plegables de 200 W. La ficha indica 3000 m2 de cobertura.'),
    ('bi-4', 'HiLight BI+ 4', 18, 4, 5, 0, 'HÍBRIDA · LED', 'Torre LED híbrida con motor diésel, baterías de iones de litio y cuatro modos de funcionamiento. Incorpora elevación hidráulica y rotación eléctrica del mástil.'),
    ('h6', 'HiLight H6+', 18, 5, 9, 0, 'DIÉSEL · LED', 'Torre LED con mástil hidráulico, motor Kubota Z482 y cobertura de 6000 m2. El fabricante presenta una carrocería protectora y acceso de servicio por un lateral.'),
    ('b6', 'HiLight B6+', 18, 6, 7, 0, 'DIÉSEL · LED', 'Torre LED con mástil hidráulico, motor Kubota Z482 y caja compacta. La tabla técnica indica cobertura de 6000 m2 y presión acústica de 55 dB(A) a 7 m.'),
    ('v4-plus', 'HiLight V4+', 18, 7, 10, 0, 'DIÉSEL · LED', 'Torre con cuatro focos LED de 250 W, carrocería HardHat® y mástil vertical manual. El catálogo indica 4000 m2 de cobertura con una media de 20 luxes.'),
    ('v4', 'HiLight V4', 18, 9, 11, 0, 'HALOGENURO METÁLICO', 'Torre diésel con cuatro focos de halogenuro metálico de 1000 W, mástil manual y puertas de acceso «alas de gaviota».'),
    ('v4w', 'HiLight V4W', 19, 2, 11, 1, 'HALOGENURO METÁLICO', 'Torre diésel con cuatro focos de halogenuro metálico de 1000 W, depósito de 160 l y mástil de 7,5 m. La tabla presenta configuraciones de 50 | 60 Hz.'),
    ('e3', 'HiLight E3+', 19, 3, 13, 0, 'ELÉCTRICA · LED', 'Torre LED eléctrica con carrocería HardHat® y mástil manual de 7 m. Puede recibir alimentación de una fuente eléctrica externa.'),
    ('pe-3', 'HiLight PE 3', 19, 4, 15, 0, 'ELÉCTRICA PORTÁTIL · LED', 'Solución LED portátil con regulación de intensidad, conexión Wi-Fi y caja de transporte. La tabla indica 3000 m2 de cobertura y mástil manual de 3 m.'),
    ('v2', 'HiLight V2+', 19, 5, 16, 1, 'ELÉCTRICA · LED', 'Torre LED eléctrica con mástil manual, bancada de acero y protecciones de polietileno. La tabla indica una potencia de iluminación de 320 W.'),
    ('v3', 'HiLight V3+', 19, 6, 16, 0, 'ELÉCTRICA · LED', 'Torre eléctrica con cuatro focos LED de 120 W, mástil manual de 5 m y protecciones de polietileno. Se conserva la cobertura indicada en la tabla técnica.')
]

new_models = []
for slug, model, page, column, image_page, image_index, tag, description in specifications:
    identifier = f'atlas-copco-hilight-{slug}'
    lighting = 'Torres de iluminación de halogenuro metálico' if slug in ('v4', 'v4w') else 'Torres de iluminación LED'
    item = base_item(identifier, model, 'equipos-auxiliares', lighting, description,
                     image_page, image_index, sorted({image_page, page}))
    item['cardTag'] = tag
    item['typeLabel'] = 'Torre de iluminación de halogenuro metálico' if slug in ('v4', 'v4w') else 'Torre de iluminación LED'
    item['groups'] = extract_groups(page, column)
    table = tables[page]
    offset = 0 if page == 18 else 1
    coverage = clean(table[2 + offset][column]).split(' ')[0]
    power = clean(table[31 + offset][column])
    height = clean(table[35 + offset][column])
    item['highlights'] = [[coverage, 'm² de cobertura'], [power, 'W de iluminación'], [height, 'm de altura máxima']]
    item['notes'].append('Las alternativas separadas por | y las unidades se conservan. Los campos vacíos o con guion del documento no se completan por suposición.')
    new_models.append(item)

by_model = {item['model']: item for item in new_models}
extra(by_model['HiLight S2+'], 6, [['Autonomía al 100% (presentación)', 'hasta 11', 'h'], ['Recarga solar indicada', '8', 'h'], ['Recarga con fuente externa indicada', '3', 'h'], ['Vida útil LED indicada', 'hasta 50 000', 'horas']])
extra(by_model['HiLight BI+ 4'], 4, [['Autonomía solo con baterías', 'hasta 19', 'h'], ['Consumo medio en modo híbrido', '0,29', 'l/h'], ['Intervalo de servicio', '1500', 'horas de iluminación']])
extra(by_model['HiLight B6+'], 7, [['Intervalo de mantenimiento', '600', 'h'], ['Vida útil LED indicada', 'hasta 50 000', 'horas']])
extra(by_model['HiLight H6+'], 9, [['Mantenimiento indicado', '40 min. cada 600 h.', ''], ['Vida útil LED indicada', 'hasta 50 000', 'horas']])
extra(by_model['HiLight V4+'], 10, [['Consumo indicado', '0,5', 'l/h'], ['Intervalo de mantenimiento', '600', 'h']])
extra(by_model['HiLight V4'], 11, [['Consumo indicado', '2', 'l/h'], ['Vida útil de lámparas indicada', 'hasta 6000', 'h']])
extra(by_model['HiLight V4W'], 11, [['Consumo indicado', '1,7', 'l/h'], ['Vida útil de lámparas indicada', 'hasta 6000', 'h']])
extra(by_model['HiLight PS 3'], 14, [['Paneles solares plegables', '2 x 200', 'W'], ['Vida útil LED indicada', '50 000', 'horas'], ['Protección indicada para focos', 'IP67 e IK10', '']])
extra(by_model['HiLight PE 3'], 15, [['Eficacia luminosa indicada', '150', 'lm/W'], ['Funciones', 'Regulación de intensidad y conexión Wi-Fi', '']])

by_model['HiLight S2+']['notes'].append('La presentación de página 6 indica hasta 11 horas al 100%; la tabla de página 18 expresa 11 | 22 h sin detallar el régimen de cada cifra.')
by_model['HiLight PS 3']['notes'].append('La tabla clasifica la fuente como Solar; el texto de página 14 indica alimentación por ZBP2000, paneles solares o fuente externa. No es un generador diésel. El asterisco de temperatura no tiene aclaración identificable en esa página.')
by_model['HiLight H6+']['notes'].append('La presentación menciona HardHat®, mientras la celda de carrocería de página 18 dice HardBody®. Se conserva la discrepancia para confirmar la configuración.')
by_model['HiLight B6+']['notes'].append('Las celdas de alternador incluyen dos juegos de potencia y de protección sin aclarar su correspondencia. Se conserva el contenido para revisión técnica.')
by_model['HiLight E3+']['notes'].append('Página 13 menciona estabilidad hasta 100 km/h, mientras la tabla de página 19 indica 80 km/h. Se presenta el valor de la tabla y se señala la diferencia; confirmar antes de operar.')
by_model['HiLight PE 3']['notes'].append('El párrafo de página 15 imprime «3000 m3»; el recuadro de esa misma página y la tabla de página 19 indican 3000 m2. Se utiliza la unidad de la tabla sin ocultar la discrepancia.')
by_model['HiLight V3+']['notes'].append('Página 19 indica 2500 m2 con media de 10 luxes. Página 16 muestra 3000 m2 con la etiqueta V2+ repetida. No se sustituye el dato de la tabla ni se asume la asignación del rótulo.')
for item in new_models:
    item['sourcePages'] = sorted(set(item['sourcePages'] + [g['page'] for g in item['groups']]))
    item['documentNote'] = 'Catálogo HiLight · páginas ' + ', '.join(map(str, item['sourcePages'])) + ' · 2023'

generators = [
    ('P2000i', '1,6', 2, 'P2000i y P2500i', [3, 1, 2]),
    ('P2500i', '2,3', 2, 'P2000i y P2500i', [4, 1, 3]),
    ('P3000', '2,3', 4, 'P3000', [4, 1, 3]),
    ('P3500i', '3', 3, 'P3500i y P6000i', [6, 1, 4]),
    ('P6000i', '6', 3, 'P3500i y P6000i', [12, None, 9]),
    ('P6500', '5', 5, 'P6500 y P8000', [10, None, 7]),
    ('P8000', '6', 5, 'P6500 y P8000', [12, None, 9])
]
for model, power, image_index, shared, quantities in generators:
    item = base_item(f'atlas-copco-{model.lower()}', model, 'generacion-de-energia', 'Grupos electrógenos',
                     f'Generador de la gama iP/P incluido en la tabla de fuentes de alimentación sugeridas. El documento indica {power} kW para {model}.', 15, image_index, [15])
    item['cardTag'], item['typeLabel'] = 'GENERADOR PORTÁTIL', 'Grupo electrógeno'
    item['highlights'] = [[power, 'kW indicados en tabla'], ['iP / P', 'gama del fabricante']]
    item['imageCaption'] = f'Imagen de la tabla, asociada a {shared}. Resolución original reducida.'
    item['groups'] = [{'title': 'Información disponible en el documento', 'page': 15,
                       'rows': [['Modelo', model, ''], ['Potencia indicada (sin clasificación PRP en esta tabla)', power, 'kW'], ['Gama', 'Generadores iP y P', '']]}]
    item['groups'].append({'title': 'Referencia de dimensionamiento de la tabla', 'page': 15,
                           'rows': [[f'HiLight {tower}: cantidad sugerida', str(quantity), ''] for tower, quantity in zip(['PE 3', 'V3+', 'E3+'], quantities) if quantity is not None]})
    item['notes'].append('Esta página no especifica motor, combustible, tensión, frecuencia, autonomía, dimensiones ni peso del generador. No se completan con datos de otros modelos.')
    item['notes'].append('Las fotografías de la tabla se comparten entre varias columnas; no acreditan la configuración de una unidad. Las cantidades de torres son una referencia de dimensionamiento del fabricante, no una garantía de compatibilidad.')
    new_models.append(item)

storage = base_item('atlas-copco-zbp2000', 'ZBP2000', 'generacion-de-energia', 'Sistemas de almacenamiento de energía',
                    'Sistema de almacenamiento de energía citado como fuente de alimentación para las torres HiLight. La tabla del fabricante indica 2 kWh; no se expresa como potencia en kW.', 15, 6, [14, 15])
storage.update(cardTag='ALMACENAMIENTO DE ENERGÍA', typeLabel='Sistema de almacenamiento de energía',
               highlights=[['2', 'kWh indicados'], ['Batería', 'fuente de alimentación']])
storage['groups'] = [{'title': 'Datos de la tabla de alimentación', 'page': 15,
                      'rows': [['Modelo', 'ZBP2000', ''], ['Energía indicada', '2', 'kWh'], ['Alimentación HiLight PE 3', '1 x 4 h.', ''], ['Alimentación HiLight V3+', '1 x 4 h.', ''], ['Alimentación HiLight E3+', '1 x 3 h.', '']]},
                     {'title': 'Aplicación descrita', 'page': 14, 'rows': [['Uso con HiLight PS 3', 'Fuente de alimentación del sistema', '']]}]
storage['notes'].append('La fuente también escribe ZBP 2000 con espacio. No aporta química de batería, tiempos de carga, peso ni dimensiones de esta unidad. Los tiempos de la tabla corresponden a las cargas indicadas.')
new_models.append(storage)

# La última página describe líneas y rangos; no identifica modelos individuales.
line_specs = [
    ('almacenamiento-extra-pequeno', 'Almacenamiento extra pequeño', 'generacion-de-energia', 'Sistemas de almacenamiento de energía', '2-10', 'kVA', 4),
    ('almacenamiento-pequeno', 'Almacenamiento pequeño', 'generacion-de-energia', 'Sistemas de almacenamiento de energía', '15-150', 'kVA', 5),
    ('almacenamiento-mediano', 'Almacenamiento mediano', 'generacion-de-energia', 'Sistemas de almacenamiento de energía', '200-500', 'kVA', 7),
    ('cargador-rapido', 'Cargador rápido', 'generacion-de-energia', 'Cargadores rápidos', '160', 'kW', 8),
    ('generadores-transportables', 'Generadores transportables', 'generacion-de-energia', 'Grupos electrógenos', '1,6-12', 'kVA', 10),
    ('generadores-especializados', 'Generadores especializados', 'generacion-de-energia', 'Grupos electrógenos', '9-660*', 'kVA', 11),
    ('generadores-versatiles', 'Generadores versátiles', 'generacion-de-energia', 'Grupos electrógenos', '9-1250*', 'kVA', 12),
    ('generadores-gran-potencia', 'Generadores de gran potencia', 'generacion-de-energia', 'Grupos electrógenos', '800–1450', 'kVA', 9),
    ('bombas-sumergibles', 'Bombas eléctricas sumergibles', 'equipos-auxiliares', 'Bombas de achique', 'hasta 18 000', 'l/min', 0),
    ('bombas-electricas-autocebantes', 'Bombas eléctricas centrífugas autocebantes', 'equipos-auxiliares', 'Bombas de achique', '833–23 300', 'l/min', 1),
    ('bombas-centrifugas-autocebantes', 'Bombas centrífugas autocebantes', 'equipos-auxiliares', 'Bombas de achique', '833–23 300', 'l/min', 13),
    ('torres-diesel', 'Torres de iluminación diésel', 'equipos-auxiliares', 'Torres de iluminación diésel', '', '', 14),
    ('torres-bateria', 'Torres de iluminación con batería', 'equipos-auxiliares', 'Torres de iluminación con batería', '', '', 3),
    ('torres-electricas', 'Torres de iluminación eléctricas', 'equipos-auxiliares', 'Torres de iluminación eléctricas', '', '', 2)
]
lines = []
for slug, name, category, equipment_type, value, unit, image_index in line_specs:
    description = f'Línea de productos Atlas Copco presentada en el cuadro general del fabricante. {("Rango indicado: " + value + " " + unit + ". ") if value else ""}No se especifican los modelos individuales en ese cuadro.'
    item = base_item(f'atlas-copco-linea-{slug}', name, category, equipment_type,
                     description, 20, image_index, [20], kind='line')
    item.update(cardTag='LÍNEA DEL FABRICANTE', typeLabel='Línea general · modelos por definir',
                highlights=[[value or 'Por definir', (unit + ' · rango de la línea') if unit else 'modelos y capacidades']],
                imageCaption='Imagen general de la línea en página 20; no representa un modelo identificado.')
    item['notes'][0] = 'Línea del catálogo del fabricante. No acredita modelos ni disponibilidad en la flota de MAQ Lavnor.'
    item['notes'].append('Marca y clasificación documentadas; modelo, configuración, prestaciones individuales y condiciones comerciales por confirmar.')
    item['groups'] = [{'title': 'Información del cuadro de productos', 'page': 20,
                       'rows': [['Línea', name, ''], ['Modelo individual', 'No especificado en este cuadro', '']] + ([['Rango indicado por el fabricante', value, unit]] if value else [])}]
    if slug.startswith('almacenamiento'):
        item['notes'].append('El cuadro de almacenamiento expresa los rangos en kVA. Se conserva esa unidad; no se convierte ni se interpreta como capacidad en kWh.')
    if '*' in value:
        item['notes'].append('El asterisco de la fuente indica múltiples configuraciones para producir energía para aplicaciones de cualquier tamaño.')
    lines.append(item)

data['equipment'] = confirmed + new_models
data['productLines'] = lines
for category in data['categories']:
    additions = [item['type'] for item in data['equipment'] + lines if item['category'] == category['id']]
    category['types'] = list(dict.fromkeys(category['types'] + additions))
(ROOT / 'data/catalogo.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
(ROOT / 'data/fuentes-atlas-tablas.json').write_text(json.dumps({'source': SOURCE, 'tables': tables}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Importados: {len(data["equipment"])} modelos y {len(lines)} líneas generales. Solo 2 modelos tienen flota confirmada.')
