"""Carga solo los nueve equipos aprobados el 10/11/2026.

Requiere pypdf y Pillow para extraer imágenes; la web publicada no usa estas
dependencias. Nunca incorpora automáticamente otros modelos de los folletos.
"""
from pathlib import Path
import json
import shutil

from PIL import Image
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
DOWNLOADS = Path.home() / 'Downloads'
data_path = ROOT / 'data/catalogo.json'
previous = json.loads(data_path.read_text(encoding='utf-8'))
previous_items = previous['equipment'] + previous.get('productLines', [])
kept = [item for item in previous['equipment'] if item['id'] in ('pramac-lsw-3y', 'atlas-copco-hilight-v5')]
assert len(kept) == 2, 'Deben conservarse las dos torres originales.'
items = []


def photo(identifier, file=None, page=None, index=None, attachment=None):
    if attachment:
        image = Image.open(DOWNLOADS / attachment)
        origin = {'file': attachment, 'kind': 'attachment'}
    else:
        image = PdfReader(DOWNLOADS / file).pages[page - 1].images[index].image
        origin = {'file': file, 'page': page, 'index': index, 'kind': 'pdf-image'}
    image = image.convert('RGBA' if 'A' in image.getbands() else 'RGB')
    if max(image.size) > 1600:
        image.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
    destination = ROOT / f'assets/images/equipos/{identifier}.webp'
    image.save(destination, 'WEBP', quality=94)
    return dict(image=destination.relative_to(ROOT).as_posix(), imageWidth=image.width,
                imageHeight=image.height, imageSource=origin)


def equipment(identifier, brand, model, category, equipment_type, type_label, tag,
              description, filename, pages, image, highlights, date='No indicada en el documento'):
    pdf_path = ROOT / f'assets/documents/{identifier}-ficha-tecnica.pdf'
    shutil.copy2(DOWNLOADS / filename, pdf_path)
    item = dict(id=identifier, brand=brand, model=model, sourceModel=model,
                category=category, type=equipment_type, typeLabel=type_label, cardTag=tag,
                kind='model', confirmed=True, description=description,
                document=pdf_path.relative_to(ROOT).as_posix(),
                documentLabel='Descargar ficha técnica',
                documentNote=f'PDF suministrado · {len(PdfReader(pdf_path).pages)} páginas',
                source=filename, sourcePages=pages, sourceDate=date,
                imageCaption='Imagen proporcionada para este equipo.' if image['imageSource']['kind'] == 'attachment' else 'Fotografía extraída de la ficha suministrada.',
                highlights=highlights, groups=[], notes=[
                    'Disponibilidad para las fechas del proyecto, tarifa, traslado y configuración de la unidad sujetos a consulta.',
                    'Las opciones del fabricante se describen por separado: su inclusión en el equipo de alquiler debe confirmarse.'], **image)
    items.append(item)
    return item


def group(item, title, page, rows, **extra):
    item['groups'].append(dict(title=title, page=page, rows=rows, **extra))


m100_file = 'Compresora de Aire_KAESER_M100.pdf'
m100 = equipment('kaeser-m100', 'KAESER', 'M100', 'equipos-de-aire', 'Compresoras', 'Compresora de aire portátil', 'AIRE COMPRIMIDO',
    'Compresora de aire portátil MOBILAIR con perfil SIGMA, caudal de 375 cfm y presión de trabajo de 100 psig en su versión básica. Incorpora motor diésel Kubota V3800, caja para herramientas y cabina galvanizada con revestimiento electrostático.',
    m100_file, [1, 2], photo('kaeser-m100', m100_file, 2, 2), [['375', 'cfm de caudal'], ['100', 'psig de trabajo'], ['96', 'hp a plena carga']])
group(m100, 'Compresor y motor · versión básica', 2, [
    ['Caudal', '375', 'cfm'], ['Presión máxima de trabajo', '100', 'psig'], ['Fabricante / modelo de motor', 'Kubota V3800', ''],
    ['Combustible', 'Diésel', ''], ['Número de cilindros', '4', ''], ['Norma de emisiones indicada', 'EPA Tier 3', ''],
    ['Potencia a plena carga', '96', 'hp'], ['Frecuencia a plena carga', '2600', 'rpm'], ['Frecuencia sin carga', '1800', 'rpm']])
group(m100, 'Equipo completo y dimensiones', 2, [
    ['Capacidad del tanque de combustible', '40', 'gal.'], ['Peso seco', '1.480', 'Kg'], ['Salidas, transcripción de la tabla', '3x ¾*; 1 x1½”', ''],
    ['Máximo nivel de ruido indicado', '76db(A) a 23 pies', ''], ['Longitud con barra de remolque', '4405', 'mm'], ['Ancho', '1780', 'mm'], ['Altura', '1515', 'mm']])
group(m100, 'Características descritas', 2, [
    ['Protección', 'Cabina galvanizada con revestimiento electrostático', ''], ['Almacenamiento', 'Caja para herramientas', ''],
    ['Control de temperatura', 'Válvula anticongelante para mantener la temperatura de trabajo y evitar la congelación de herramientas', ''],
    ['Depósito', 'Tanque de combustible de gran tamaño para operación prolongada', '']])
group(m100, 'Opciones del fabricante · por confirmar', 2, [
    ['Presiones opcionales', 'Hasta 205', 'psi'], ['Tratamiento de aire opcional', 'Posenfriador y paquetes de filtración', ''], ['Montaje opcional', 'Sobre trineo (skid)', '']])
m100['notes'].append('La presión opcional de hasta 205 psi no sustituye la presión de la versión básica de 100 psig. La fila de salidas contiene un asterisco tras ¾; confirmar conexión exacta.')

m235_file = 'Compresora de Aire_KAESER_M235.pdf'
m235 = equipment('kaeser-m235', 'KAESER', 'M235', 'equipos-de-aire', 'Compresoras', 'Compresora de aire portátil', 'AIRE COMPRIMIDO',
    'Compresora de aire portátil MOBILAIR con perfil SIGMA, caudal de 825 cfm y presión máxima de trabajo de 125 psig según la tabla suministrada. Cuenta con chasis de alta resistencia, cabina galvanizada y caja de herramientas.',
    m235_file, [1, 2], photo('kaeser-m235', m235_file, 2, 1), [['825', 'cfm de caudal'], ['125', 'psig de trabajo'], ['260', 'hp a plena carga']])
group(m235, 'Compresor y motor', 2, [
    ['Caudal', '825', 'cfm'], ['Presión máxima de trabajo', '125', 'psig'], ['Motor, denominación de la tabla', 'Cummis QSB 6.7 T', ''],
    ['Tipo de motor', 'Diésel', ''], ['Potencia a plena carga', '260', 'hp'], ['Frecuencia a plena carga', '2000', 'rpm'], ['Frecuencia sin carga', '1200', 'rpm']])
group(m235, 'Equipo completo y dimensiones', 2, [
    ['Capacidad del tanque de combustible', '119', 'gal.'], ['Peso seco', '3230', 'Kg.'], ['Salida', 'No especificada en la celda del documento', ''],
    ['Máximo nivel de ruido indicado', '76 db(A) a 23 ft.', ''], ['Longitud con barra de remolque', '5207', 'mm.'], ['Ancho', '1770', 'mm.'], ['Altura', '2182', 'mm.']])
group(m235, 'Características descritas', 2, [
    ['Chasis', 'Alta resistencia', ''], ['Cabina', 'Galvanizada con revestimiento electrostático', ''], ['Almacenamiento', 'Caja para herramientas', ''],
    ['Control de temperatura', 'Válvula anticongelante para mantener la temperatura de trabajo y evitar la congelación de herramientas', ''],
    ['Depósito', 'Tanque de combustible de gran tamaño', '']])
group(m235, 'Opciones del fabricante · por confirmar', 2, [
    ['Presiones opcionales', 'Hasta 200', 'psi'], ['Tratamiento de aire opcional', 'Posenfriador y paquetes de filtración', ''], ['Montaje opcional', 'Sobre trineo (skid)', '']])
m235['notes'].append('La fuente escribe «Cummis QSB 6.7» en características y «Motor Cummis QSB 6.7 T» en la tabla. Se conserva esa denominación sin corregirla por suposición. La conexión de salida no está especificada.')

tex_file = 'Martillo Neumático_ATLAS COPCO_TEXP60S.pdf'
tex = equipment('atlas-copco-tex-p60s', 'ATLAS COPCO', 'TEX P60S', 'complementos', 'Martillos neumáticos', 'Martillo neumático silenciado', 'DEMOLICIÓN NEUMÁTICA',
    'Martillo neumático silenciado para trabajos de demolición y rotura de pavimentos. La ficha indica 1500 golpes/min y consumo de aire de 36 l/s (76 cfm), con palanca SOFSTART de dos etapas, acoplamiento pivotante y lubricador integrado.',
    tex_file, [2, 3, 4], photo('atlas-copco-tex-p60s', attachment='131-Martillo-TEX-60-Atlas-Copco-800x800.png'),
    [['1500', 'golpes/min'], ['33', 'kg de peso'], ['36', 'l/s de aire']], '© 2005 · código de impresión 2006 07')
group(tex, 'Rendimiento · TEX P60S', 2, [
    ['Presión de aire de referencia de la tabla', '90 lbs/pulg2 (6 bares)', ''], ['Peso', '33 kg (73 lb)', ''],
    ['Consumo de aire', '36 l/s (76 cfm)', ''], ['Longitud', '692 mm (27 1/4”)', ''], ['Frecuencia de impacto', '1500', 'Golpes/min'], ['Versión', 'S = silenced (silenciado)', '']])
group(tex, 'Variantes de culata / conexión · por confirmar', 2, [
    ['Culata de herramienta, variante 1', '28x160 mm (1 1/8” x 6”)', ''], ['Designación de variante 1', '8461 0227 22', ''],
    ['Culata de herramienta, variante 2', '32x160 mm (1 1/4” x 6”)', ''], ['Designación de variante 2', '8461 0227 23', ''],
    ['Portaherramientas, norma Atlas Copco', '9000 0306 00', ''], ['Portaherramientas, norma US', '9001 0005 06', '']])
group(tex, 'Diseño y control', 3, [
    ['Carcasa', 'Construcción sólida de una pieza', ''], ['Arranque', 'Palanca SOFSTART de dos etapas', ''], ['Conexión', 'Acoplamiento pivotante que gira bajo presión', ''],
    ['Mecanismo', 'Yunque para reducir desgaste del pistón y cilindro', ''], ['Retorno del pistón', 'Con cojín de aire', ''],
    ['Lubricación', 'Lubricador integrado, admite aceites minerales o sintéticos', '']])
group(tex, 'Herramientas descritas · inclusión por confirmar', 4, [
    ['Familias compatibles descritas', 'Cincel pica; plano estrecho; plano ancho; para asfalto; para cavar; de pala; de pala redondeado; cincel cuña; vástago para placas pisón; placas pisón redonda y cuadrada', ''],
    ['Selección de herramienta', 'Confirmar norma y dimensiones de culata antes de elegir el accesorio', '']])
tex['notes'].append('Se publica únicamente TEX P60S. El folleto también describe P60, P90 y P90S; sus datos no se atribuyen a este modelo ni se añaden como equipos.')
tex['notes'].append('La imagen adjunta se usa para TEX P60S; confirmar cuál de las dos variantes de culata corresponde a la unidad. La presión indicada es la condición de referencia de la tabla.')

hydro_file = 'Martillo Hidraulico-HYDROKHAN-UG3300.pdf'
hydro = equipment('hydrokhan-ug3300', 'HYDROKHAN', 'UG3300', 'complementos', 'Martillos hidráulicos', 'Martillo hidráulico', 'DEMOLICIÓN HIDRÁULICA',
    'Martillo hidráulico UG3300 con peso operativo de 2700 kg, herramienta de 158 mm y velocidad de impacto indicada entre 250 y 600 bpm. El folleto describe un flujo de aceite de 180 a 250 l/min; la selección de excavadora y conexiones requiere confirmar la configuración.',
    hydro_file, [1], photo('hydrokhan-ug3300', attachment='Martillo-hydrokhan-ug-3300.png'), [['2700', 'kg de peso operativo'], ['158', 'mm de herramienta'], ['250 ~ 600', 'bpm de impacto']])
group(hydro, 'Características técnicas', 1, [
    ['Peso operativo', '2700', 'kg'], ['Longitud total', '2780 mm (109 in)', ''], ['Flujo de aceite requerido', '180 ~ 250 l/min (47.5 ~ 63.4 gpm)', ''],
    ['Presión de operación', '160 ~ 180 kg/cm2 (2276 ~ 2560 psi)', ''], ['Velocidad de impacto', '250 ~ 600', 'bpm'],
    ['Diámetro de herramienta', '158 mm (6.22 in)', ''], ['Diámetro de manguera, transcripción del original', '1, 1/4', 'in']])
group(hydro, 'Aplicación y valores de impacto · ver observaciones', 1, [
    ['Excavadora aplicable, rótulo inferior del folleto', '29 - 38', 'Ton'], ['Equipo aplicable, celda de tabla', '29 ~ 38', 'l/min'],
    ['Valor de impacto, rótulo original «Frecuencia de Impacto»', '1383', 'kg.m'],
    ['Valor de impacto, rótulo original «Frecuencia de Impacto»', '10000', 'ft.lbs'],
    ['Valor de impacto, rótulo original «Frecuencia de Impacto»', '13558', 'joules']])
hydro['notes'].append('El cuadro «Equipo Aplicable» usa l/min para 29 ~ 38, mientras el rótulo inferior dice «EXCAVADORA 29 - 38 Ton». Se muestran ambas referencias y se requiere confirmar la compatibilidad con la excavadora.')
hydro['notes'].append('La fuente titula «Frecuencia de Impacto» los valores en kg.m, ft.lbs y joules. Se conserva el rótulo y sus unidades sin presentarlos como golpes/min; la velocidad indicada separadamente es 250 ~ 600 bpm.')
hydro['notes'].append('El diámetro de manguera aparece como «1, 1/4 in». Confirmar dimensión y conexión exactas antes de la instalación.')

cat_file = 'Minicargador CAT_243D.pdf'
cat = equipment('cat-246d', 'CAT', '246D', 'movimiento-de-tierras', 'Minicargadores', 'Minicargador de levantamiento radial', 'MOVIMIENTO DE TIERRAS',
    'Minicargador CAT 246D de levantamiento radial, equipado con motor Cat C3.3B DIT turbo. La ficha indica capacidad nominal de operación de 975 kg y potencia bruta de 55,4 kW (74,3 hp). Cuenta con transmisión hidrostática y acceso a los puntos de servicio a nivel del suelo.',
    cat_file, [1, 2, 3, 4], photo('cat-246d', cat_file, 1, 0), [['975', 'kg de capacidad nominal'], ['55,4', 'kW de potencia bruta'], ['3.368', 'kg en orden de trabajo']], 'ASHQ7130-01 · 08-13 · traducción 11-13')
group(cat, 'Motor', 1, [
    ['Modelo de motor', 'Cat C3.3B DIT (turbo)', ''], ['Potencia bruta SAE J1995', '55,4 kW / 74,3 hp', ''],
    ['Potencia neta SAE 1349', '53,6 kW / 71,8 hp', ''], ['Potencia neta SAE 1349, variante †', '54,0 kW / 72,4 hp', ''],
    ['Potencia neta ISO 9249', '54,1 kW / 72,6 hp', ''], ['Potencia neta ISO 9249, variante †', '54,6 kW / 73,2 hp', ''],
    ['Par máximo a 1.600 rpm SAE J1995', '265 N·m / 195 lbf-pie', ''], ['Cilindrada', '3,3 L / 203 pulg3', ''],
    ['Carrera', '120 mm / 4,7”', ''], ['Calibre', '94 mm / 3,7”', '']])
group(cat, 'Peso, desplazamiento y capacidad', 1, [
    ['Peso en orden de trabajo', '3.368 kg / 7.424 lb', ''], ['Velocidad de desplazamiento, una velocidad', '12,5 km/h / 7,7 mph', ''],
    ['Velocidad con opción de dos velocidades', '17,7 km/h / 11,0 mph', ''], ['Capacidad nominal de operación', '975 kg / 2.150 lb', ''],
    ['Capacidad nominal con contrapeso optativo', '1.088 kg / 2.400 lb', ''], ['Carga límite de equilibrio', '1.950 kg / 4.300 lb', ''],
    ['Fuerza de desprendimiento del cilindro de inclinación', '3.336 kg / 7.355 lb', '']])
group(cat, 'Sistema hidráulico', 1, [
    ['Presión del cargador, flujo estándar', '23.000 kPa / 3.335 lb/pulg²', ''], ['Flujo del cargador, estándar', '86 L/min / 23 gal EE.UU./min', ''],
    ['Potencia hidráulica calculada, estándar', '33 kW / 44 hp', ''], ['Presión máxima, alto caudal XPS opcional', '28.000 kPa / 4.061 lb/pulg²', ''],
    ['Flujo máximo, alto caudal XPS opcional', '121 L/min / 32 gal EE.UU./min', ''], ['Potencia hidráulica calculada, XPS opcional', '57 kW / 76 hp', '']])
group(cat, 'Cabina y capacidades de llenado', 1, [
    ['ROPS', 'ISO 3471:2008', ''], ['FOPS nivel I', 'ISO 3449:2005 nivel I', ''], ['FOPS nivel II, referencia indicada', 'ISO 3449:2005 nivel II', ''],
    ['Caja de cadena, cada lado', '12,7 L / 3,3 gal EE.UU.', ''], ['Sistema de enfriamiento', '14 L / 3,7 gal EE.UU.', ''],
    ['Cárter del motor', '11 L / 3,0 gal EE.UU.', ''], ['Tanque de combustible', '94 L / 24,8 gal EE.UU.', ''],
    ['Sistema hidráulico', '52 L / 13,7 gal EE.UU.', ''], ['Tanque hidráulico', '39 L / 10,3 gal EE.UU.', '']])
group(cat, 'Dimensiones de la configuración de referencia', 2, [
    ['1. Distancia entre ejes', '1.249 mm / 49,2”', ''], ['2. Longitud sin cucharón', '2.993 mm / 117,8”', ''],
    ['3. Longitud con cucharón sobre el suelo', '3.708 mm / 146,0”', ''], ['4. Altura hasta la parte superior de la cabina', '2.110 mm / 83,1”', ''],
    ['5. Altura total máxima', '4.032 mm / 158,7”', ''], ['6. Altura del pasador a levantamiento máximo', '3.154 mm / 124,2”', ''],
    ['7. Altura del pasador en posición de acarreo', '200 mm / 7,9”', ''], ['8. Alcance a levantamiento y descarga máximos', '600 mm / 23,6”', ''],
    ['9. Espacio libre a levantamiento y descarga máximos', '2.465 mm / 97,1”', ''], ['10. Espacio libre sobre el suelo', '226 mm / 8,9”', ''],
    ['11. Ángulo de salida', '26°', ''], ['12. Proyección del parachoques detrás del eje trasero', '1.083 mm / 42,6”', ''],
    ['13. Ángulo de descarga máximo', '39°', ''], ['14. Ancho sobre ruedas', '1.676 mm / 66”', ''],
    ['15. Radio de giro al extremo trasero', '1.806 mm / 71,2”', ''], ['16. Radio de giro al acoplador', '1.401 mm / 55,2”', ''],
    ['17. Radio de giro al cucharón', '2.181 mm / 85,9”', ''], ['18. Alcance máximo con brazos paralelos al suelo', '1.388 mm / 54,6”', ''],
    ['19. Ángulo de inclinación hacia atrás a altura máxima', '96°', '']])
group(cat, 'Equipamiento de serie descrito', 3, [
    ['Sistema eléctrico', '12 voltios; alternador de 80 amperios; batería de 880 CCA; llave de arranque/parada; iluminación de trabajo; alarma de retroceso', ''],
    ['Puesto del operador', 'Medidores de combustible y horas; asiento de vinilo ajustable; posabrazos abatible; espejo; toma de 12 voltios; bocina; acelerador de mano electrónico; joysticks ajustables; almacenamiento', ''],
    ['Control y protección', 'Traba de sistema hidráulico/transmisión/freno al abandonar el asiento o levantar el posabrazos; cabina ROPS abierta abatible; FOPS nivel I; ventanas superior y trasera; sistema antirrobo con teclado', ''],
    ['Tren de fuerza', 'Motor Cat C3.3B turbo; filtro de aire de doble elemento; transmisión hidrostática; tracción por cadena a las cuatro ruedas; frenos de estacionamiento por resorte y desconexión hidráulica', ''],
    ['Servicio y auxiliares', 'Filtros hidráulicos tipo cartucho; separador de agua/combustible; radiador/enfriador de aceite lado a lado; válvula de muestreo S·O·S; mirillas de aceite y refrigerante; manguera ToughGuard; auxiliares de flujo continuo', ''],
    ['Otros elementos', 'Recinto de motor trabable; anticongelante -36 °C (-33 °F); seis puntos de amarre; soporte de brazo; desconexiones rápidas de superficie plana con alivio de presión; salida para baliza; ventilador de velocidad variable', '']])
group(cat, 'Paquetes y opciones del fabricante · por confirmar', 3, [
    ['Selecciones de configuración', 'Hidráulico estándar o XPS; acoplador eléctrico o mecánico; cinturón 50 mm (2”) o 75 mm (3”); una o dos velocidades con variantes de amortiguación', ''],
    ['Paquete H1', 'Flujo estándar sin nivelación automática', ''], ['Paquete H3', 'Alto caudal XPS, autonivelación bidireccional y amortiguación eléctrica', ''],
    ['Paquete H4', 'Flujo estándar, retorno a excavación y amortiguación electrónica', ''],
    ['Comodidad C0 / C1', 'ROPS abierta con alternativas de asiento y equipamiento', ''], ['Comodidad C2 / C3', 'Cabina cerrada con calefacción / cabina con aire acondicionado', ''],
    ['Accesorios opcionales', 'Contrapesos; baliza; calentador de bloque 120 V; operación en frío; pintura especial; batería 1.000 CCA; Product Link celular', ''],
    ['Control y confort opcionales', 'Pantalla avanzada LCD de 5”; cámara trasera; retorno a excavación; radio Bluetooth con USB y entrada auxiliar; asiento neumático con calefacción', '']])
cat['notes'].append('El archivo se llama CAT_243D, pero todas sus páginas identifican 246D. El usuario confirmó expresamente CAT 246D; no se publican datos como si fueran de un 243D.')
cat['notes'].append('Los valores † corresponden al motor equivalente Tier 4 Interim para Canadá, Australia/Nueva Zelanda, Macedonia, Ucrania y Corea del Sur, según la nota de la ficha. No se asumen para la unidad disponible.')
cat['notes'].append('Peso, capacidad y dimensiones de referencia: operador de 75 kg (165 lb), todos los fluidos, una velocidad, OROPS, cucharón de 1.676 mm (66 in), neumáticos PC Cat 12 × 16.5, flujo estándar, asiento mecánico, sin contrapesos y acoplador manual, salvo indicación contraria.')

bob_file = 'Minicargador-BOBCAT-S650.pdf'
bob = equipment('bobcat-s650', 'BOBCAT', 'S650', 'movimiento-de-tierras', 'Minicargadores', 'Minicargador', 'MOVIMIENTO DE TIERRAS',
    'Minicargador Bobcat S650 con motor diésel D24, capacidad nominal estipulada de 1253 kg y sistema hidráulico de 87.10 L/min. La ficha describe transmisión hidrostática, bastidor Bob-Tach y sistema de bloqueo interfuncional BICS.',
    bob_file, [1], photo('bobcat-s650', attachment='Minicargador S650.jpg'), [['1253', 'kg de capacidad nominal'], ['56.0', 'kW a 2600 r.p.m.'], ['3657', 'kg de peso operativo']], '2016-9-28 · B2LA 11001 — B2LA 99999')
group(bob, 'Capacidad e hidráulica', 1, [
    ['Capacidad nominal estipulada (ISO 14397-1)', '1253', 'kg'], ['Carga de vuelco', '2507', 'kg'], ['Capacidad de la bomba', '87.10', 'L/min'],
    ['Capacidad con alto caudal opcional', '115.50', 'L/min'], ['Alivio en acopladores rápidos', '23.8-24.5', 'MPa'], ['Velocidad máxima, primera velocidad', '11.4', 'km/h']])
group(bob, 'Motor y pesos', 1, [
    ['Marca / modelo', 'Bobcat/D24', ''], ['Cumplimiento indicado', '97/68 CE Fase IIIB', ''], ['Combustible', 'Diésel', ''], ['Refrigeración', 'Líquida', ''],
    ['Potencia SAE J1995 a 2600 r.p.m.', '56.0', 'kW'], ['Par SAE J1995 bruto a 1800 r.p.m.', '283.9', 'Nm'], ['Cilindros', '4', ''], ['Cilindrada', '2392', 'cm3'],
    ['Depósito de combustible', '90.50', 'L'], ['Peso operativo', '3657', 'kg'], ['Peso de envío', '3344', 'kg']])
group(bob, 'Mandos y transmisión', 1, [
    ['Dirección y velocidad', 'Dos palancas manuales', ''], ['Elevación e inclinación', 'Pedales; ACS opcional o controles SJC independientes', ''],
    ['Auxiliar delantero estándar', 'Interruptor eléctrico en palanca manual derecha', ''],
    ['Transmisión', 'Bombas de pistones hidrostáticos en tándem infinitamente variables, con dos motores hidrostáticos completamente reversibles', '']])
group(bob, 'Equipamiento de serie descrito', 1, [
    ['Puesto del operador', 'Asiento ajustable con suspensión y respaldo largo; cabina Deluxe con ventanillas; instrumentación; barra de asiento; cinturón de seguridad', ''],
    ['Sistema hidráulico y acople', 'Caudal variable/máximo; Bob-Tach; auxiliar delantero proporcional eléctrico; autonivelación de cuchara con selección de encendido/apagado', ''],
    ['Protección y operación', 'BICS; parada de hidráulico/motor; soporte de brazos; freno de estacionamiento; luces delanteras/traseras; bujías automáticas; turbocompresor con apagachispas', ''],
    ['Neumáticos de serie', '12 x 16,5, 12 lonas, para tareas duras', ''], ['ROPS', 'SAE-J1040 e ISO 3471', ''], ['FOPS nivel I', 'SAE-J1043 e ISO 3449', ''], ['Certificación indicada', 'CE', '']])
group(bob, 'Opciones del fabricante · por confirmar', 1, [
    ['Transmisión y acople', 'Dos velocidades; alto caudal; Bob-Tach hidráulico', ''], ['Cabina y confort', 'Tablero Deluxe; cabina cerrada con calefacción; aire acondicionado; asientos neumáticos y cinturón de 2 o 3 puntos', ''],
    ['Controles opcionales', 'Sistema de control avanzado ACS; controles de joystick seleccionables SJC', ''],
    ['Neumáticos opcionales', '33 x 15.5-16,5 de superflotación; 12 x 16,5 para tareas o condiciones duras con distintas llantas, Poly Fill o Solid Flex', ''],
    ['Otros opcionales', 'Alarma de marcha atrás; girofaro; calentador de bloque; extintor; luz estroboscópica', '']])
group(bob, 'Aspectos ambientales indicados', 1, [
    ['Operador LpA (98/37 y 474-1)', '85', 'dB(A)'], ['Ruido LWA, Directiva UE 2000/14/CE', '101', 'dB(A)'],
    ['Vibración de cuerpo completo, ISO 2631–1', '0.90', 'ms-2'], ['Vibración mano/brazo, ISO 5349–1', '1.40', 'ms-2']])
bob_diagram = photo('bobcat-s650-dimensiones', bob_file, 1, 1)
group(bob, 'Dimensiones · códigos del esquema original', 1, [
    [letter, value, unit] for letter, value, unit in [
        ('A', '4026.0', 'mm'), ('B', '2065.0', 'mm'), ('C', '25.0', '°'), ('D', '207.0', 'mm'), ('E', '1150.0', 'mm'),
        ('F', '2754.0', 'mm'), ('G', '3474.0', 'mm'), ('H', '30.0', '°'), ('I', '2447.0', 'mm'), ('J', '3149.0', 'mm'),
        ('K', '800.0', 'mm'), ('L', '42.0', '°'), ('M', '97.0', '°'), ('N', '1880.0', 'mm'), ('O', '2106.0', 'mm'),
        ('P', '1507.0', 'mm'), ('Q', '1832.0', 'mm')]], diagram=bob_diagram['image'], diagramCaption='Esquema original Bobcat S650. Las letras corresponden a la tabla de dimensiones.')
bob['notes'].append('Las dimensiones conservan las letras A–Q del esquema, sin inventar nombres para cotas no rotuladas. Las unidades de vibración se transcriben como ms-2, tal como están impresas.')
bob['notes'].append('La lista de implementos y las condiciones de garantía del folleto no constituyen inventario ni condiciones comerciales de MAQ Lavnor. Confirmar implemento y configuración requeridos.')

dyn_file = 'Rodillo-DYNAPAC-DTR75.pdf'
dyn = equipment('dynapac-dtr75', 'DYNAPAC', 'DTR75', 'movimiento-de-tierras', 'Rodillos dúplex', 'Rodillo dúplex de compactación', 'COMPACTACIÓN',
    'Rodillo dúplex Dynapac DTR75 con transmisión hidrostática, vibración en ambos tambores y motor Hatz 1D 42 refrigerado por aire. La ficha indica peso operativo de 757 kg, fuerza centrífuga de 22 kN y ancho de tambor de 650 mm.',
    dyn_file, [1, 2], photo('dynapac-dtr75', dyn_file, 1, 1), [['757', 'kg de peso operativo'], ['22', 'kN de fuerza centrífuga'], ['650', 'mm de tambor']], '2020-12-22 19:20')
group(dyn, 'Peso y tracción', 1, [
    ['Peso operativo', '757', 'kg'], ['Peso neto', '727', 'kg'], ['Carga por eje, media', '379', 'kg'],
    ['Velocidad 1, adelante / atrás', '5,5', 'km/h'], ['Velocidad 2, adelante / atrás', '2,5', 'km/h'],
    ['Pendiente máxima sin vibración', '40', '%'], ['Pendiente máxima con vibración', '35', '%']])
group(dyn, 'Compactación', 1, [['Amplitud nominal', '0.45', 'mm'], ['Frecuencia', '55', 'Hz'], ['Fuerza centrífuga', '22', 'kN']])
group(dyn, 'Motor y sistema hidráulico', 1, [
    ['Fabricante / modelo', 'Hatz 1D 42', ''], ['Cilindros', '1', ''], ['Tanque de combustible', '5,0', 'l'], ['Consumo de combustible, unidad de la fuente', '1,3', 'l'],
    ['Emisiones indicadas', 'no EPA', ''], ['Depósito de agua', '60', 'l'], ['Potencia', '6,2 kW (8,4 cv) a 2800 rpm', ''], ['Refrigeración', 'Por aire', ''],
    ['Transmisión', 'Hidrostático', ''], ['Frenos de servicio', 'Hidrostático', ''], ['Freno de estacionamiento', 'Mecánica', '']])
dyn_diagram = photo('dynapac-dtr75-dimensiones', dyn_file, 2, 1)
group(dyn, 'Dimensiones', 2, [
    ['A. Distancia entre ejes', '550', 'mm'], ['B. Ancho', '762', 'mm'], ['C. Altura libre', '200', 'mm'], ['D. Diámetro del tambor', '400', 'mm'],
    ['H. Altura', '960', 'mm'], ['H1. Altura', '1210', 'mm'], ['K. Distancia libre al suelo, módulo delantero', '110', 'mm'], ['L. Longitud', '2200', 'mm'],
    ['L1. Longitud', '2320', 'mm'], ['O. Saliente', '20', 'mm'], ['S. Espesor de tambor', '8', 'mm'], ['W. Ancho de tambor', '650', 'mm']],
    diagram=dyn_diagram['image'], diagramCaption='Esquema original DTR75, con referencias a las cotas de la tabla.')
group(dyn, 'Equipamiento estándar descrito', 2, [
    ['Riego y regulación', 'Equipo de riego; velocidad variable; regulación de vibración y aceleración en barra de dirección', ''],
    ['Barra de dirección', 'Altura regulable; aislamiento de vibraciones; protección de marcha atrás', ''],
    ['Compactación', 'Vibración mecánica con excéntrica en ambos tambores; dos rascadores en cada tambor', ''],
    ['Seguridad y servicio', 'Control con freno de estacionamiento; parada automática por bajo nivel de aceite; punto único de elevación', ''],
    ['Arranque', 'Eléctrico y con manivela', '']])
dyn['notes'].append('El fabricante denomina DTR75 «rodillo dúplex». Se conserva esa clasificación; no se presenta como un rodillo tándem tripulado.')
dyn['notes'].append('El consumo está impreso como 1,3 l sin base temporal. No se transforma en l/h ni se calcula autonomía a partir de ese dato.')

for item in kept:
    item.update(kind='model', confirmed=True)
    item['notes'] = [note for note in item['notes'] if 'resto de la gama' not in note or 'flota confirmada' not in note]

approved = kept + items
assert len(approved) == 9
assert len({item['id'] for item in approved}) == 9
categories = [
    dict(id='movimiento-de-tierras', name='Movimiento de tierras', icon='earth', description='Preparación del terreno y compactación.', types=['Minicargadores', 'Rodillos dúplex']),
    dict(id='equipos-auxiliares', name='Equipos auxiliares', icon='light', description='Iluminación para cada frente de trabajo.', types=['Torres de iluminación LED']),
    dict(id='generacion-de-energia', name='Equipos de generación de energía', icon='power', description='Energía temporal para tu operación.', types=['Grupos electrógenos']),
    dict(id='equipos-de-aire', name='Equipos de aire', icon='air', description='Aire comprimido para el trabajo en campo.', types=['Compresoras']),
    dict(id='complementos', name='Complementos', icon='hammer', description='Herramientas para ampliar tu capacidad.', types=['Martillos hidráulicos', 'Martillos neumáticos', 'Martillos fragmentadores']),
    dict(id='unidades-livianas', name='Unidades livianas', icon='truck', description='Movilidad para el equipo de trabajo.', types=['Camionetas'])]
data_path.write_text(json.dumps(dict(categories=categories, equipment=approved, catalogRevision='2026-11-10'), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# Retirar solo los HTML e imágenes de registros anteriores excluidos por el usuario.
retained_ids = {item['id'] for item in approved}
retained_images = {item['image'] for item in approved}
removed = []
for old in previous_items:
    if old['id'] in retained_ids:
        continue
    for candidate in [ROOT / f'equipos/{old["id"]}.html', ROOT / old['image']]:
        target = candidate.resolve()
        assert target.is_relative_to(ROOT.resolve()), target
        if target.is_file() and target.relative_to(ROOT).as_posix() not in retained_images:
            target.unlink()
            removed.append(str(target.relative_to(ROOT)))
print(f'Catálogo aprobado: {len(approved)} equipos. Archivos antiguos retirados: {len(removed)}.')
