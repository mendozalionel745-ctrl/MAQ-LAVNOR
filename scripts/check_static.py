"""Revisa enlaces internos, recursos, anclas y estructura de las páginas publicables."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
PAGES = [ROOT / 'index.html', ROOT / 'catalogo.html', ROOT / 'nosotros.html', ROOT / 'cotizacion.html', *sorted((ROOT / 'equipos').glob('*.html'))]


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.ids = []
        self.references = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if 'id' in values:
            self.ids.append(values['id'])
        if tag == 'script':
            assert values.get('src'), 'Script inline inesperado'
        assert tag != 'style', 'CSS inline inesperado'
        if tag == 'img':
            assert 'alt' in values, 'Imagen sin atributo alt'
        for key in ['href', 'src']:
            if values.get(key):
                self.references.append(values[key])


parsed = {p.resolve(): Page(p.read_text(encoding='utf-8')) for p in PAGES}
count = 0
for path, page in parsed.items():
    text = path.read_text(encoding='utf-8')
    assert '{{' not in text, f'Plantilla sin completar: {path}'
    assert len(page.ids) == len(set(page.ids)), f'IDs duplicados: {path}'
    for reference in page.references:
        url = urlsplit(reference)
        if url.scheme or url.netloc:
            continue
        target = (path.parent / unquote(url.path)).resolve() if url.path else path
        assert target.is_relative_to(ROOT), f'Ruta fuera del sitio: {reference}'
        assert target.is_file(), f'Recurso faltante: {reference} en {path.name}'
        if url.fragment and target in parsed:
            assert unquote(url.fragment) in parsed[target].ids, f'Ancla faltante: {reference}'
        count += 1
print(f'{len(PAGES)} páginas; {count} enlaces, recursos y anclas internos correctos. Sin IDs duplicados ni plantillas pendientes.')
