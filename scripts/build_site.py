"""Genera el HTML estático desde plantillas y datos. Solo requiere Python estándar."""
from pathlib import Path
from html import escape
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'data/catalogo.json').read_text(encoding='utf-8'))
EQUIPMENT = DATA['equipment']
CATEGORIES = DATA['categories']
ALL_ITEMS = EQUIPMENT
CATEGORY_NAMES = {category['id']: category['name'] for category in CATEGORIES}

# Cada icono tiene un archivo propio para funcionar también al abrir index.html.
ET.register_namespace('', 'http://www.w3.org/2000/svg')
icon_directory = ROOT / 'assets/images/icons'
icon_directory.mkdir(exist_ok=True)
for symbol in ET.parse(ROOT / 'assets/images/icons.svg').getroot().findall('.//{http://www.w3.org/2000/svg}symbol'):
    svg = ET.Element('{http://www.w3.org/2000/svg}svg', {'viewBox': symbol.attrib['viewBox']})
    svg.extend(list(symbol))
    ET.ElementTree(svg).write(icon_directory / f'{symbol.attrib["id"]}.svg', encoding='unicode')


def e(value):
    return escape(str(value), quote=True)


def template(name, values):
    text = (ROOT / f'templates/{name}.html').read_text(encoding='utf-8')
    for key, value in values.items():
        text = text.replace('{{' + key + '}}', str(value))
    return text


def icon(name, prefix=''):
    return f'<img class="equipment-icon" src="{prefix}assets/images/icons/{e(name)}.svg" width="64" height="48" alt="" loading="lazy">'


def card(item):
    search = e(' '.join([item['brand'], item['model'], item['type'], CATEGORY_NAMES[item['category']]]))
    highlights = ''.join(f'<div><dt>{e(label)}</dt><dd>{e(value)}</dd></div>' for value, label in item['highlights'][:2])
    confirmed = item.get('confirmed', False)
    status = 'Flota confirmada' if confirmed else 'Fabricante · disponibilidad por confirmar'
    photo_class = ' low-resolution' if item.get('lowResolution') else ''
    return f'''<article class="equipment-card" data-category="{e(item['category'])}" data-type="{e(item['type'])}" data-kind="{e(item.get('kind', 'model'))}" data-confirmed="{str(confirmed).lower()}" data-search="{search}">
      <a class="equipment-image{photo_class}" href="equipos/{e(item['id'])}.html" tabindex="-1" aria-hidden="true"><span class="image-tag">{e(item.get('cardTag', item['type']))}</span><img src="{e(item['image'])}" width="{item['imageWidth']}" height="{item['imageHeight']}" loading="lazy" alt=""></a>
      <div class="equipment-body"><p class="equipment-brand">{e(item['brand'])}</p><h3><a href="equipos/{e(item['id'])}.html">{e(item['model'])}<span aria-hidden="true">↗</span></a></h3><p class="equipment-type">{e(item.get('typeLabel', item['type']))}</p><p class="catalog-status{' is-confirmed' if confirmed else ''}">{status}</p><dl class="card-specs">{highlights}</dl><div class="card-actions"><a class="text-link" href="equipos/{e(item['id'])}.html">{'Ver información' if item.get('kind') == 'line' else 'Ver ficha técnica'} <span aria-hidden="true">→</span></a><a class="small-quote" href="cotizacion.html?equipo={e(item['id'])}" aria-label="Consultar {e(item['brand'])} {e(item['model'])}">{'Cotizar' if confirmed else 'Consultar'} ↗</a></div></div></article>'''


def write_page(filename, page, title, description, content, prefix='', scripts=''):
    values = dict(title=e(title), description=e(description), content=content, prefix=prefix,
                  scripts=scripts, bodyClass=e(page), homeCurrent='', catalogCurrent='', contactCurrent='', aboutCurrent='')
    values[{'home': 'homeCurrent', 'catalog': 'catalogCurrent', 'detail': 'catalogCurrent', 'quote': 'contactCurrent', 'about': 'aboutCurrent'}[page]] = 'aria-current="page"'
    destination = ROOT / filename
    destination.parent.mkdir(parents=True, exist_ok=True)
    rendered = template('layout', values)
    destination.write_text('\n'.join(line.rstrip() for line in rendered.splitlines()) + '\n', encoding='utf-8')
    print(f'Generado: {filename}')


category_cards = []
for index, category in enumerate(CATEGORIES, 1):
    count = sum(item['category'] == category['id'] for item in EQUIPMENT)
    status = f'{count} equipos con ficha técnica' if count else 'Modelos por documentar'
    types = ' · '.join(e(t) for t in category['types'][:3])
    if len(category['types']) > 3:
        types += ' · Y más equipos'
    category_cards.append(f'''<a class="category-card" href="catalogo.html?categoria={category['id']}"><div class="category-card-top">{icon(category['icon'])}<span class="category-number">0{index}</span></div><h3>{e(category['name'])}</h3><p>{types}</p><div class="category-card-bottom"><span>{status}</span><span class="category-arrow" aria-hidden="true">↗</span></div></a>''')

write_page('index.html', 'home', 'MAQ Lavnor | Alquiler de maquinaria en Perú',
           'Explora las líneas de equipos de MAQ Lavnor: movimiento de tierras, iluminación LED, energía, aire, complementos y unidades livianas.',
           template('inicio', {'categories': ''.join(category_cards), 'modelCount': len(EQUIPMENT),
               'featured': ''.join(card(x) for x in EQUIPMENT)}))

filters = ''.join(f'<button class="filter-button" type="button" data-filter="{c["id"]}" aria-pressed="false">{e(c["name"])} <span aria-hidden="true">↗</span></button>' for c in CATEGORIES)
types = ''.join(f'<option>{e(t)}</option>' for c in CATEGORIES for t in c['types'])
pending = []
for category in CATEGORIES:
    if any(item['category'] == category['id'] for item in ALL_ITEMS):
        continue
    links = ''.join(f'<a href="cotizacion.html?tipo={e(t)}">Consultar {e(t.lower())} <span aria-hidden="true">↗</span></a>' for t in category['types'])
    pending.append(f'''<article class="pending-family" data-category="{category['id']}" data-types="{e('|'.join(category['types']))}" data-search="{e(category['name'] + ' ' + ' '.join(category['types']))}">{icon(category['icon'])}<span class="pending-label">INFORMACIÓN TÉCNICA PENDIENTE</span><h3>{e(category['name'])}</h3><p>{' · '.join(e(t) for t in category['types'])}</p><p class="pending-description">Marca, modelo, fotografía y especificaciones por completar.</p><div class="pending-links">{links}</div></article>''')

write_page('nosotros.html', 'about', 'Nosotros | MAQ Lavnor',
           'Conoce MAQ Lavnor: alquiler de maquinaria, nuestros valores y una mirada a nuestras entregas de equipos.',
           template('nosotros', {}))

write_page('catalogo.html', 'catalog', 'Catálogo de equipos | MAQ Lavnor',
           'Explora los equipos de MAQ Lavnor: torres de iluminación, compresoras, martillos, minicargadores y compactación. Consulta la ficha de cada modelo.',
           template('catalogo', {'filters': filters, 'types': types, 'cards': ''.join(card(x) for x in ALL_ITEMS), 'pending': ''.join(pending),
               'modelCount': len(EQUIPMENT)}),
           scripts='<script defer src="assets/js/catalogo.js"></script>')

for item in ALL_ITEMS:
    values = {key: e(value) for key, value in item.items() if isinstance(value, (str, int))}
    values.update(categoryName=e(CATEGORY_NAMES[item['category']]),
                  typeLabel=e(item.get('typeLabel', item['type'])),
                  imageCaption=e(item.get('imageCaption', 'Fotografía referencial del fabricante.')),
                  imageClass=' low-resolution' if item.get('lowResolution') else '',
                  availability=('Flota confirmada · disponibilidad para tus fechas: consultar' if item.get('confirmed') else
                      ('Línea del fabricante · modelos y disponibilidad por confirmar' if item.get('kind') == 'line' else 'Catálogo del fabricante · disponibilidad por confirmar')),
                  quoteLabel='Cotizar este equipo' if item.get('confirmed') else 'Consultar este producto')
    values['highlights'] = ''.join(f'<div><strong>{e(value)}</strong><span>{e(label)}</span></div>' for value, label in item['highlights'])
    tables = []
    for group in item['groups']:
        if group.get('diagram'):
            tables.append(f'<figure class="technical-diagram"><a href="../{e(group["diagram"])}" target="_blank" rel="noopener"><img src="../{e(group["diagram"])}" loading="lazy" alt="{e(group.get("diagramCaption", group["title"]))}"></a><figcaption>{e(group.get("diagramCaption", group["title"]))} Abre la imagen para ampliarla.</figcaption></figure>')
        rows = ''.join(f'<tr><th scope="row">{e(label)}</th><td>{e(value)}{(" " + e(unit)) if unit else ""}</td></tr>' for label, value, unit in group['rows'])
        tables.append(f'<table class="spec-table"><caption>{e(group["title"])}<span>Fuente: pág. {group["page"]}</span></caption><tbody>{rows}</tbody></table>')
    values['tables'] = ''.join(tables)
    values['notes'] = ''.join(f'<li>{e(note)}</li>' for note in item['notes'])
    values['sourcePages'] = ', '.join(str(page) for page in item['sourcePages'])
    write_page(f'equipos/{item["id"]}.html', 'detail', f'{item["brand"]} {item["model"]} | MAQ Lavnor', item['description'], template('equipo', values), prefix='../')

equipment_options = ''
for label, items in [('Equipos del catálogo · disponibilidad para fechas sujeta a consulta', EQUIPMENT)]:
    equipment_options += f'<optgroup label="{e(label)}">' + ''.join(f'<option value="{e(item["id"])}" data-status="{e(label)}">{e(item["brand"])} {e(item["model"])}</option>' for item in items) + '</optgroup>'
type_options = '<optgroup label="Consulta por tipo de equipo">' + ''.join(f'<option value="{e(t)}">{e(t)}</option>' for c in CATEGORIES for t in c['types']) + '</optgroup>'
write_page('cotizacion.html', 'quote', 'Cotización y contacto | MAQ Lavnor',
           'Prepara una consulta de alquiler con el modelo, ubicación y plazo de tu proyecto. Canales comerciales pendientes de completar.',
           template('cotizacion', {'equipmentOptions': equipment_options, 'typeOptions': type_options}),
           scripts='<script defer src="assets/js/config.js"></script><script defer src="assets/js/cotizacion.js"></script>')
