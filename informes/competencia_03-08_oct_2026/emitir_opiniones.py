# -*- coding: utf-8 -*-
"""Documento de análisis y opiniones — acompaña al Reporte de Competencia 10-15 Oct 2026.

Es un documento SEPARADO del informe. El informe presenta datos; este presenta
lecturas, juicios y recomendaciones, y declara en cada punto qué está verificado
y qué no.

Fuentes:
  - Tablas del propio informe (cruces y aritmética: analisis_aereo_10-15.json).
  - analisis_familia_reputacion.json: 21 agentes con búsqueda web (rutas aéreas,
    políticas de equipaje, reputación hotelera, dos simulaciones de decisión).
    ADVERTENCIA: las dos pasadas de verificación adversarial y la síntesis no
    alcanzaron a ejecutarse. Todo lo que viene de ahí va marcado y las
    afirmaciones se contrastaron a mano contra las tablas del informe; una
    afirmación falsa detectada así ("Maryland no está a la venta") fue eliminada.

Uso:  python3 emitir_opiniones.py
"""
import base64, os, subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
CHROME = '/opt/pw-browsers/chromium'

def b64(path, mime):
    with open(os.path.join(AQUI, path), 'rb') as f:
        return f'data:{mime};base64,' + base64.b64encode(f.read()).decode()

LOGO = b64('marca/logo_decameron.png', 'image/png')

# ---------------------------------------------------------------------------
CSS = '''
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin:0; padding:0; }
body { font-family:'Segoe UI','DejaVu Sans',Arial,sans-serif; color:#16324A; }
.page { width:210mm; height:297mm; padding:11mm 13mm 13mm; page-break-after:always;
        position:relative; background:#fff; }
.page:last-child { page-break-after:auto; }

/* portada */
.portada { padding:0; display:flex; flex-direction:column; }
.pt-top { background:linear-gradient(135deg,#16324A 0%,#003A6F 55%,#0077B5 100%);
          flex:1; display:flex; flex-direction:column; justify-content:center;
          align-items:center; text-align:center; padding:22mm 20mm; position:relative; }
.pt-top::after { content:''; position:absolute; left:0; right:0; bottom:0; height:3mm;
                 background:#E08A1E; }
.pt-logo { width:78mm; background:#fff; padding:5mm 6mm; border-radius:2mm; margin-bottom:11mm; }
.pt-kicker { color:#9ED4E9; font-size:9.5pt; letter-spacing:.28em; margin-bottom:5mm; }
.pt-top h1 { color:#fff; font-size:31pt; line-height:1.12; letter-spacing:.01em; }
.pt-top h1 span { color:#E08A1E; }
.pt-sub { color:#ACE3F5; font-size:12pt; margin-top:6mm; line-height:1.5; max-width:135mm; }
.pt-bot { background:#fff; padding:14mm 20mm; }
.pt-bot h3 { font-size:10pt; color:#003A6F; letter-spacing:.14em; margin-bottom:4mm; }
.pt-bot p { font-size:9.3pt; color:#4A5C6E; line-height:1.62; text-align:justify; margin-bottom:3.5mm; }
.pt-bot b { color:#16324A; }
.pt-meta { display:flex; gap:9mm; margin-top:7mm; padding-top:5mm; border-top:1px solid #D6DFE7;
           font-size:8pt; color:#878787; }
.pt-meta b { color:#16324A; display:block; font-size:9pt; margin-bottom:.8mm; }

/* cabecera de página */
.head { display:flex; align-items:center; gap:5mm; border-bottom:2.2px solid #003A6F;
        padding-bottom:2.5mm; margin-bottom:6mm; }
.head img { height:8.5mm; }
.head .t { font-size:7.6pt; color:#878787; letter-spacing:.05em; }
.head .t b { color:#16324A; }
.head .tag { margin-left:auto; background:#FBF2DF; color:#B05C00; border:1px solid #E8CE96;
             font-size:6.8pt; letter-spacing:.14em; padding:1.2mm 3.5mm; border-radius:1mm; }
.foot { position:absolute; bottom:7mm; left:14mm; right:14mm; display:flex;
        justify-content:space-between; font-size:7pt; color:#878787;
        border-top:.5px solid #D6DFE7; padding-top:1.8mm; }

h2.sec { font-size:15pt; color:#003A6F; letter-spacing:.01em; margin-bottom:1.5mm; line-height:1.2; }
.sec-sub { font-size:8pt; color:#878787; letter-spacing:.04em; margin-bottom:4mm;
           padding-bottom:2mm; border-bottom:1px solid #D6DFE7; }
h3.blk { font-size:10.3pt; color:#16324A; margin:4mm 0 2mm; }
h3.blk::before { content:''; display:inline-block; width:3mm; height:3mm; background:#E08A1E;
                 margin-right:2.5mm; border-radius:.5mm; vertical-align:-.2mm; }
p { font-size:8.7pt; line-height:1.52; color:#3E5265; margin-bottom:2.4mm; text-align:justify; }
p b, li b { color:#16324A; }
.lead { font-size:9.8pt; line-height:1.48; color:#16324A; margin-bottom:4mm; }
ul { margin:0 0 4mm 0; padding-left:4.5mm; }
li { font-size:8.6pt; line-height:1.48; color:#3E5265; margin-bottom:1.8mm; }

table { width:100%; border-collapse:collapse; font-size:7.8pt; margin-bottom:2.5mm; }
th { background:#16324A; color:#fff; font-size:6.9pt; letter-spacing:.07em; text-transform:uppercase;
     padding:2mm 2.2mm; text-align:right; font-weight:600; }
th:first-child { text-align:left; }
td { padding:1.4mm 2.2mm; border-bottom:.5px solid #D6DFE7; text-align:right;
     font-variant-numeric:tabular-nums; }
td:first-child { text-align:left; font-weight:600; color:#16324A; }
tr.dec td { background:#EFF7FC; }
tr.dec td:first-child { color:#003A6F; }
.bien { color:#15793C; font-weight:700; }
.mal { color:#BF382A; font-weight:700; }
.gris { color:#878787; }
caption, .tcap { caption-side:bottom; font-size:6.7pt; color:#878787; text-align:left;
                 padding-top:1.5mm; line-height:1.45; }

.caja { border:1px solid #D6DFE7; border-left:4px solid #0077B5; background:#F7FBFD;
        padding:3mm 4mm; margin-bottom:3mm; border-radius:0 1.5mm 1.5mm 0; }
.caja.alerta { border-left-color:#D43C29; background:#FDF5F3; }
.caja.ok { border-left-color:#1A9C4A; background:#F4FBF6; }
.caja.ambar { border-left-color:#E08A1E; background:#FDF8EF; }
.caja h4 { font-size:9.1pt; color:#16324A; margin-bottom:1.5mm; }
.caja p { font-size:8.3pt; line-height:1.48; margin-bottom:1.2mm; }
.caja p:last-child { margin-bottom:0; }

.kpis { display:flex; gap:3.5mm; margin-bottom:5mm; }
.kpi { flex:1; border:1px solid #D6DFE7; border-radius:1.5mm; padding:3.5mm; text-align:center;
       background:#fff; }
.kpi .n { font-size:17.5pt; font-weight:700; color:#003A6F; line-height:1.1; }
.kpi .n.r { color:#BF382A; } .kpi .n.g { color:#15793C; } .kpi .n.a { color:#B05C00; }
.kpi .l { font-size:7.2pt; color:#878787; letter-spacing:.05em; margin-top:1.5mm; line-height:1.4; }

.dos { display:flex; gap:5mm; }
.dos > div { flex:1; }
.persona { border:1px solid #D6DFE7; border-radius:1.5mm; overflow:hidden; margin-bottom:4mm; }
.persona .ph { background:#16324A; color:#fff; padding:2.5mm 4mm; font-size:9.4pt; font-weight:600; }
.persona .ph span { display:block; font-size:7.4pt; color:#9ED4E9; font-weight:400; margin-top:.6mm; }
.persona .pb { padding:3.5mm 4mm; }
.persona .pb p { font-size:8.3pt; line-height:1.5; margin-bottom:1.8mm; }
.veredicto { background:#FBF2DF; border-top:1px solid #E8CE96; padding:2.5mm 4mm;
             font-size:8.6pt; color:#5C4310; }
.veredicto b { color:#16324A; }

ol.rec { counter-reset:r; list-style:none; padding:0; }
ol.rec li { counter-increment:r; position:relative; padding-left:9mm; margin-bottom:2.8mm;
            font-size:8.6pt; line-height:1.48; }
ol.rec li::before { content:counter(r); position:absolute; left:0; top:-.3mm; width:6mm; height:6mm;
  background:#003A6F; color:#fff; border-radius:50%; font-size:8pt; font-weight:700;
  display:flex; align-items:center; justify-content:center; }
ol.rec li b { display:block; color:#16324A; font-size:9.5pt; margin-bottom:.8mm; }
'''

def head(tag='Análisis y opiniones'):
    return (f'<div class="head"><img src="{LOGO}"><div class="t">'
            f'<b>DOCUMENTO DE ANÁLISIS</b> · Competencia 10 – 15 Octubre 2026</div>'
            f'<div class="tag">{tag}</div></div>')

def foot(txt, n):
    return f'<div class="foot"><span>{txt}</span><span>{n}</span></div>'

def page(cuerpo, pie, n, tag='Análisis y opiniones'):
    return f'<div class="page">{head(tag)}{cuerpo}{foot(pie,n)}</div>'

# ---------------------------------------------------------------------------
PORTADA = f'''<div class="page portada">
  <div class="pt-top">
    <img src="{LOGO}" class="pt-logo">
    <div class="pt-kicker">DOCUMENTO COMPLEMENTARIO · NO ES EL REPORTE</div>
    <h1>Qué dicen los números<br><span>cuando se cruzan</span></h1>
    <div class="pt-sub">Análisis, lecturas y recomendaciones sobre el Reporte de
      Competencia del 10 al 15 de octubre de 2026</div>
  </div>
  <div class="pt-bot">
    <h3>PARA QUÉ SIRVE ESTE DOCUMENTO</h3>
    <p>El reporte de competencia muestra <b>precios</b>. Este documento muestra lo que
      esos precios significan cuando se cruzan entre sí, contra la categoría real de cada
      hotel, contra su reputación pública y contra lo que un cliente vive al comprar.
      Son <b>opiniones fundadas en datos</b>, no cifras adicionales del informe: por eso
      van en un documento aparte y no dentro de las tablas.</p>
    <p><b>Cada afirmación declara su respaldo.</b> Lo que sale de la aritmética del propio
      informe es verificable línea a línea. Lo que sale de fuentes externas —categorías,
      puntajes, rutas aéreas, políticas de equipaje— se levantó con búsqueda web el
      31/08/2026 y va marcado con su nivel de confianza. Las dos verificaciones
      adversariales previstas no alcanzaron a ejecutarse, así que el contraste se hizo a
      mano contra las tablas: una afirmación falsa detectada así fue descartada antes de
      llegar a esta página.</p>
    <div class="pt-meta">
      <div><b>31/08/2026</b>Fecha de análisis</div>
      <div><b>V.3</b>Informe de referencia</div>
      <div><b>21 fuentes</b>Rutas, tarifas y reputación</div>
      <div><b>$943</b>Conversión CLP→USD</div>
    </div>
  </div>
</div>'''

# ---------------------------------------------------------------------------
P_CANAL = '''
<h2 class="sec">Lo que el informe muestra y nadie había leído</h2>
<div class="sec-sub">Tres patrones que aparecen al cruzar las columnas entre sí · aritmética del propio informe, verificable</div>

<div class="kpis">
  <div class="kpi"><div class="n">19/19</div><div class="l">FILAS DONDE FALABELLA<br>Y DESPEGAR SON IGUALES</div></div>
  <div class="kpi"><div class="n g">−10,7%</div><div class="l">VENTAJA MECÁNICA<br>DE COCHA EN SAN ANDRÉS</div></div>
  <div class="kpi"><div class="n r">+23,5%</div><div class="l">DESVÍO DE EXPEDIA<br>SOLO EN HOTELES PROPIOS</div></div>
</div>

<h3 class="blk">Falabella y Despegar son la misma vitrina</h3>
<p>En las <b>19 filas con precio de las tablas de alojamiento por destino no hay una sola
diferencia</b> entre V. Falabella y Despegar. Ni un dólar, ni en hoteles propios ni en
competencia. Solo se separan en paquetería, y ahí la diferencia es el componente aéreo. Eso
significa que ambas cuentas se alimentan de la misma carga tarifaria: no hay diferenciación
de precio hotelero entre ellas, y <b>toda corrección de carga impacta a las dos a la vez</b>
—lo que es una ventaja operativa, no un problema, siempre que sea intencional.</p>

<h3 class="blk">Cocha vende lo nuestro un 11% más barato, y es estructural</h3>
<p>En los cinco Decameron de San Andrés la ventaja de Cocha es de <b>−10,6% a −11,0%</b>.
Esa regularidad no es una promoción puntual: un descuento comercial varía por hotel, un
porcentaje idéntico en cinco propiedades sale de una <b>condición estructural</b> —comisión
distinta o tarifa neta distinta—. El promedio sobre los ocho hoteles propios comparables es
−12,6%, con Los Cabos en −32%.</p>
<table>
  <tr><th>Hotel propio</th><th>Falabella / Despegar</th><th>Cocha</th><th>Brecha</th></tr>
  <tr class="dec"><td>Decameron Isleño</td><td>$1,642</td><td>$1,467</td><td class="mal">−10,7%</td></tr>
  <tr class="dec"><td>Decameron San Luis</td><td>$954</td><td>$852</td><td class="mal">−10,7%</td></tr>
  <tr class="dec"><td>Decameron Marazul</td><td>$1,066</td><td>$951</td><td class="mal">−10,8%</td></tr>
  <tr class="dec"><td>Decameron Maryland</td><td>$1,246</td><td>$1,114</td><td class="mal">−10,6%</td></tr>
  <tr class="dec"><td>Decameron Los Delfines</td><td>$1,344</td><td>$1,196</td><td class="mal">−11,0%</td></tr>
  <tr class="dec"><td>Grand Decameron Complex</td><td>$1,304</td><td>$1,163</td><td class="mal">−10,8%</td></tr>
  <tr class="dec"><td>Grand Decameron Los Cabos</td><td>$2,174</td><td>$1,479</td><td class="mal">−32,0%</td></tr>
</table>
<p class="tcap">Alojamiento, 10–15 oct, 2 adultos, USD. La columna Falabella/Despegar es idéntica en las dos vitrinas.</p>

<h3 class="blk">Expedia no está cara: nuestra carga está mal</h3>
<p>Es la distinción que cambia la conclusión. Expedia aparece más cara en todo el informe,
pero al separar hoteles propios de competencia el desvío <b>solo existe en los nuestros</b>:
<b>+23,5% promedio en Decameron contra +0,2% en la competencia</b> de las mismas tablas. Si
Expedia fuera simplemente un canal caro, ambos grupos subirían igual. No es un problema de
canal: es un problema de carga tarifaria propia en ese canal.</p>
<table>
  <tr><th>Hotel</th><th>Falabella</th><th>Expedia</th><th>Desvío</th></tr>
  <tr class="dec"><td>Decameron Isleño</td><td>$1,642</td><td>$2,687</td><td class="mal">+63,6%</td></tr>
  <tr class="dec"><td>Decameron Marazul</td><td>$1,066</td><td>$1,748</td><td class="mal">+64,0%</td></tr>
  <tr class="dec"><td>Decameron Maryland</td><td>$1,246</td><td>$1,810</td><td class="mal">+45,3%</td></tr>
  <tr><td>Dorado Plaza (competencia)</td><td>$1,132</td><td>$1,162</td><td>+2,7%</td></tr>
  <tr><td>Grand Sirenis (competencia)</td><td>$2,248</td><td>$2,274</td><td>+1,2%</td></tr>
  <tr><td>Porto Horizonte (competencia)</td><td>$1,758</td><td>$1,756</td><td class="bien">−0,1%</td></tr>
</table>
'''

P_COCHA = '''
<div class="caja ambar">
  <h4>La única excepción confirma la regla — y avisa algo</h4>
  <p>Tras recotizar <b>Decameron Barú</b> el 31/08, su celda de V. Falabella quedó en
  <b>$2,142</b> contra los <b>$1,928</b> de Despegar, que son del 27/08. Es el único caso de
  todo el informe donde no coinciden, y no prueba que los canales difieran: prueba que
  <b>la tarifa se movió $214 en cuatro días</b>. La paridad que se observa en el resto es de
  una foto tomada el mismo día; conviene no leerla como una condición permanente sin
  confirmarlo.</p>
</div>

<h2 class="sec">El hallazgo más grave no es de precio</h2>
<div class="sec-sub">Los hoteles existen en Cocha, tienen cupo y tarifa — y no aparecen en la búsqueda</div>

<div class="caja alerta">
  <h4>Dos de los cuatro NA no eran NA</h4>
  <p>Grand Decameron Panamá y Decameron Galeón figuraban sin tarifa o desactualizados en
  Cocha. Al entrar <b>por hotel y fecha</b> —en vez de por búsqueda de destino— los dos
  tenían tarifa disponible: <b>$963</b> y <b>$1,461</b>. No estaban sin cupo. No se
  exhibían.</p>
  <p>El Galeón lo confirma de forma concluyente: Cocha vendía su <b>paquete a $3,357</b>
  mientras mostraba «sin disponibilidad» en alojamiento. Si vende el paquete, hay
  habitaciones. La celda equivocada era la de alojamiento.</p>
</div>

<p>Hay que separar dos cosas que se confunden fácil, porque tienen tamaños muy distintos.</p>

<div class="caja alerta">
  <h4>La exhibición: el problema es de TODOS, no de dos</h4>
  <p><b>Ningún hotel Decameron de este informe se obtuvo desde la búsqueda de destino de
  Cocha.</b> Los diez, sin excepción, hubo que encontrarlos escribiendo el nombre del hotel.
  Ni en alojamiento ni en paquetería aparecen navegando por destino, que es como busca un
  cliente que todavía no eligió hotel.</p>
  <p>Eso no afecta la exactitud de las celdas —los precios de Cocha en estas páginas son
  correctos—, pero sí significa que <b>en la práctica no estamos en esa góndola</b> para
  quien no nos busca por nombre. Y quien ya nos busca por nombre es un cliente que la marca
  ya ganó.</p>
</div>

<div class="caja ok">
  <h4>La disponibilidad: ahí sí se parte en dos, y hay buenas noticias</h4>
  <p>De los cuatro hoteles que figuraban NA, <b>dos tenían tarifa</b> (Panamá $963 y el
  Galeón $1,461) y <b>dos están genuinamente sin cupo</b> (Cartagena y Punta Sal),
  verificados también por hotel y fecha. Con eso el informe queda con <b>todas sus celdas de
  Cocha revisadas una por una</b>: un NA en estas páginas ya no significa «el buscador no me
  mostró nada», significa que se entró al hotel, se pusieron las fechas y no había
  habitaciones.</p>
</div>

<p>Y hay una lectura comercial que ninguna tabla de este informe puede mostrar, porque las
tablas comparan precios: <b>un cliente que busca «Panamá» o «Santa Marta» en Cocha no
encuentra el hotel</b>. No es que lo vea caro y elija otro. No lo ve. Está pagando el costo
de estar en el canal sin recibir la exhibición.</p>

<div class="caja">
  <h4>Por qué esto vale más que cualquier diferencia de tarifa del informe</h4>
  <p>Una brecha de precio del 11% se corrige negociando. Un hotel invisible en la góndola
  no vende <b>a ningún precio</b>. Todo el esfuerzo de este reporte —afinar tarifas,
  comparar contra la competencia, discutir paridad— asume que el cliente <i>ve</i> el hotel.
  En dos destinos verificados, no lo ve.</p>
</div>

<h3 class="blk">Qué preguntarle a Cocha</h3>
<p>La pregunta no es por qué faltan dos hoteles, sino <b>por qué ninguna de las diez fichas
Decameron aparece en la búsqueda de destino</b> —incluidas las de San Andrés y México, que
sí tienen tarifa y cupo—. Puede ser un tema de indexación, de cómo están clasificadas las
fichas o de filtros por defecto del buscador. Sea cual sea, es una conversación técnica
concreta y no una negociación de tarifa: se resuelve sin ceder un peso de margen.</p>

<div class="caja ambar">
  <h4>Además: falta una fila entera</h4>
  <p>En la tabla de <b>paquetería de Cartagena</b>, Decameron Cartagena no tenía fila: solo
  aparecían los tres competidores. Ya se agregó como NA en la V.3, pero conviene revisar por
  qué se perdió — un hotel propio ausente de su propia tabla de destino es un error que
  cambia cómo se lee el bloque completo.</p>
</div>
'''

P_ESTRELLAS = '''
<h2 class="sec">Estrellas y puntuación: la premisa, revisada</h2>
<div class="sec-sub">Categoría comercial y reseñas públicas · levantado con búsqueda web el 31/08/2026 · confianza media, sin verificación adversarial</div>

<p class="lead">La lectura habitual es que competimos contra hoteles de 4 y 5 estrellas y
por eso salimos más baratos. <b>Es cierto en la mitad de los casos y falso en la otra
mitad</b> — y donde es cierto, la estrella extra casi nunca se traduce en mejores reseñas.</p>

<h3 class="blk">Dónde la premisa NO se cumple: Cartagena</h3>
<p>Los dos hoteles que aparecen más baratos en la tabla de Cartagena y que arrastran el
promedio hacia abajo <b>son de 3 estrellas</b>, no de 4 ni 5:</p>
<table>
  <tr><th>Hotel</th><th>Estrellas</th><th>Reputación</th><th>Precio</th></tr>
  <tr><td>Hotel Dorado Plaza Bocagrande</td><td class="mal">3★</td><td>Booking 6,9</td><td>$967</td></tr>
  <tr><td>Hotel La Gran Vía</td><td class="mal">3★</td><td>TripAdvisor 4,0 (247)</td><td>$580</td></tr>
  <tr><td>Hotel Cartagena Dubai</td><td>4★</td><td>TripAdvisor 3,0 (888) · #97/284</td><td>$587</td></tr>
  <tr><td>Hotel Cartagena Plaza</td><td>4★</td><td>TripAdvisor 4,0 (6.874) · <b>#13/284</b></td><td>NA</td></tr>
  <tr class="dec"><td>Decameron Cartagena</td><td>3–4★</td><td>TripAdvisor 3,0 (3.084) · #69/284</td><td>NA</td></tr>
</table>
<p class="tcap">Precio = mejor tarifa OTA de alojamiento, 10–15 oct. Categorías verificadas en Booking/Kayak; en Colombia la clasificación por estrellas no es obligatoria, por eso varía entre plataformas.</p>
<p>Comparar un todo incluido de playa contra <b>hoteles urbanos de 3 estrellas</b> no es
comparar el mismo producto. Cuando la tabla dice que La Gran Vía es «el más económico» a
$580, no está diciendo que seamos caros: está diciendo que el bloque mezcla dos categorías
de producto distintas. Vale la pena revisar el set de comparables de ese destino.</p>

<h3 class="blk">Dónde sí se cumple, y ahí duele</h3>
<table>
  <tr><th>Destino</th><th>Nuestro hotel</th><th>Competidor</th><th>Estrellas</th><th>Booking</th></tr>
  <tr class="dec"><td>Panamá</td><td>Grand Decameron $963</td><td>—</td><td>4★</td><td class="mal">7,6 (2.323)</td></tr>
  <tr><td>Panamá</td><td>—</td><td>Riu Playa Blanca $1,059</td><td>5★</td><td class="bien">8,4 (3.103)</td></tr>
  <tr><td>Panamá</td><td>—</td><td>Gran Evenia Bijao $788</td><td>«5»★</td><td class="bien">8,3 (2.058)</td></tr>
  <tr><td>Panamá</td><td>—</td><td>Dreams Playa Bonita $1,207</td><td>4,5★</td><td>7,8 (755)</td></tr>
  <tr class="dec"><td>Santa Marta</td><td>Galeón $1,461</td><td>—</td><td class="mal">3★</td><td>7,9 (~110)</td></tr>
  <tr><td>Santa Marta</td><td>—</td><td>Porto Horizonte $1,756</td><td>4★</td><td>8,1 (389)</td></tr>
  <tr><td>Santa Marta</td><td>—</td><td>Irotama del Sol (NA)</td><td>5★</td><td class="gris">no verificado</td></tr>
</table>
<div class="caja alerta">
  <h4>Panamá: somos el último de los cuatro en Booking</h4>
  <p>En el destino con <b>vuelo directo desde Santiago</b> —el mejor argumento logístico de
  todo el informe— nuestro hotel tiene el puntaje más bajo de su tabla. El Riu, 5 estrellas
  y 8,4 con 3.103 reseñas, está a <b>$96 de distancia por toda la estadía</b>: menos de $20
  por noche. Y el Bijao, con 8,3, cuesta <b>$175 menos</b> que nosotros.</p>
</div>

'''
P_MATIZ = '''
<h2 class="sec">El matiz que juega a favor</h2>
<div class="sec-sub">La estrella extra del competidor no siempre es real · y dónde sí lo es</div>
<p>La estrella extra del competidor <b>a menudo no es real</b>. En San Andrés, Sol Caribe
San Andrés y El Dorado son 4 estrellas comerciales y puntúan <b>3,0 en TripAdvisor</b>,
exactamente igual que nuestros hoteles; sus propias reseñas dicen que «se siente de 2-3
estrellas». El Gran Evenia Bijao se vende como 5 estrellas y las guías coinciden en que el
producto real es 3,5.</p>
<p>Las excepciones reales son <b>Grand Sirenis San Andrés</b> (5★, TripAdvisor 4,0, #3 de 86)
y <b>Riu Playa Blanca</b> (5★, Booking 8,4). Contra el resto no estamos peor posicionados de
lo que dice nuestro precio —<b>pero el cliente que solo mira estrellitas no lo sabe, y nadie
se lo explica</b>.</p>

<h3 class="blk">Nuestra mejor carta está subvalorada</h3>
<p><b>Decameron Maryland</b> es el mejor calificado de los cinco de San Andrés: Google 4,4
(1.806 reseñas), TripAdvisor 4,0 (#3 de 84) y Booking 7,8 — el único de la nómina propia
que rompe el techo de 3,0 en TripAdvisor. Cuesta $1,114, por debajo del Isleño ($1,467) que
puntúa 3,0. Si hay un hotel que merece destacarse en la vitrina de la isla, es ese.</p>

<div class="caja ok">
  <h4>La conclusión práctica del capítulo</h4>
  <p>El relato «nos comparan contra 4 y 5 estrellas» <b>no alcanza para explicar la brecha
  de precio</b>: en Cartagena la competencia es de 3 estrellas, y en San Andrés la de 4
  estrellas puntúa igual que nosotros. Donde sí perdemos de verdad es contra los dos 5
  estrellas reales del informe —Grand Sirenis y Riu— y ahí la diferencia no es de etiqueta:
  es de reseñas.</p>
</div>

'''

P_VALOR = '''
<h2 class="sec">El precio no siempre conversa con el producto</h2>
<div class="sec-sub">Contraste entre destinos sobre la mejor tarifa OTA de alojamiento</div>

<p class="lead">Dentro de cada tabla los precios se ven razonables. El problema aparece al
mirarlos <b>entre destinos</b>, que es exactamente lo que hace un cliente que todavía no
decidió a dónde va.</p>


<table>
  <tr><th>Hotel</th><th>Destino</th><th>Categoría</th><th>Reputación</th><th>Precio</th></tr>
  <tr><td>Grand Sirenis San Andrés</td><td>San Andrés</td><td>5★ real</td><td>TA 4,0 · #3/86</td><td>$1,942</td></tr>
  <tr class="dec"><td>Decameron Isleño</td><td>San Andrés</td><td>3–4★</td><td class="mal">TA 3,0 (3.286)</td><td>$1,467</td></tr>
  <tr class="dec"><td>Decameron Galeón</td><td>Santa Marta</td><td class="mal">3★</td><td>Booking 7,9 (~110)</td><td>$1,461</td></tr>
  <tr class="dec"><td>Decameron Maryland</td><td>San Andrés</td><td>3–4★</td><td class="bien">TA 4,0 · #3/84</td><td>$1,114</td></tr>
  <tr><td>Riu Playa Blanca</td><td>Panamá</td><td>5★ real</td><td class="bien">Booking 8,4 (3.103)</td><td>$1,059</td></tr>
  <tr class="dec"><td>Grand Decameron Panamá</td><td>Panamá</td><td>4★</td><td>Booking 7,6 (2.323)</td><td>$963</td></tr>
  <tr><td>Gran Evenia Bijao</td><td>Panamá</td><td>«5»★ (real 3,5)</td><td class="bien">Booking 8,3 (2.058)</td><td>$788</td></tr>
</table>

<div class="caja alerta">
  <h4>Isleño y Galeón cuestan ~38% más que un 5 estrellas mejor puntuado</h4>
  <p>El <b>Isleño ($1,467)</b> y el <b>Galeón ($1,461)</b> están <b>39% y 38% por encima</b>
  del Riu Playa Blanca ($1,059), que es 5 estrellas verificado y puntúa 8,4 con 3.103
  reseñas. Son destinos distintos y eso importa —el aéreo cambia la ecuación—, pero un
  cliente que compara «todo incluido en el Caribe» ve las dos fichas en la misma pantalla.</p>
  <p>El caso del <b>Galeón</b> es el más expuesto: <b>3 estrellas verificadas</b>, con apenas
  ~110 opiniones en Booking, a precio de 5 estrellas de otro destino.</p>
</div>

'''
P_PAQUETE = '''
<h2 class="sec">Y el paquete a veces castiga al cliente</h2>
<div class="sec-sub">Alojamiento contra paquetería, contrastado con armar el viaje a mano</div>
<p>Cruzando alojamiento contra paquetería y restando, se puede reconstruir cuánto cobra cada
operador por el aéreo. Comparado contra armar el viaje por separado con la mejor tarifa
aérea del propio informe:</p>
<table>
  <tr><th>Hotel</th><th>Armar por separado</th><th>Paquete</th><th>Diferencia</th></tr>
  <tr class="dec"><td>Decameron Galeón</td><td>$2,329</td><td>$3,357</td><td class="mal">paquete +$1,028</td></tr>
  <tr class="dec"><td>Grand Decameron Complex</td><td>$2,575</td><td>$3,097</td><td class="mal">paquete +$522</td></tr>
  <tr class="dec"><td>Grand Decameron Panamá</td><td>$2,123</td><td>$2,273</td><td class="mal">paquete +$150</td></tr>
  <tr class="dec"><td>Decameron San Luis</td><td>$1,620</td><td>$1,697</td><td>paquete +$77</td></tr>
  <tr class="dec"><td>Decameron Maryland</td><td>$1,882</td><td>$1,894</td><td class="gris">empate</td></tr>
  <tr class="dec"><td>Decameron Los Delfines</td><td>$1,964</td><td>$1,886</td><td class="bien">paquete −$78</td></tr>
  <tr class="dec"><td>Decameron Isleño</td><td>$2,235</td><td>$2,074</td><td class="bien">paquete −$161</td></tr>
</table>
<p class="tcap">«Armar por separado» = mejor tarifa de alojamiento del informe + 2 pasajes a la tarifa aérea más baja de la tabla de aéreos. Ambas columnas para 2 adultos, USD.</p>

<p><b>El paquete del Galeón cuesta $1,028 más que armarlo a mano.</b> Cualquier cliente con
una pestaña de Google Flights abierta lo detecta en diez minutos — y quien descubre una fila
así deja de confiar en el precio empaquetado de <i>toda</i> la marca, no solo de ese hotel.
Cuando el paquete está bien armado (Isleño −$161, Los Delfines −$78) hace exactamente lo que
debe: convierte.</p>

<div class="caja">
  <h4>Un detalle técnico que conviene mirar</h4>
  <p>Cocha construye sus paquetes de San Andrés como hotel + <b>$424–425 por persona,
  idéntico en los cinco hoteles</b>. Un aéreo real varía según la disponibilidad del día:
  un valor fijo repetido en cinco propiedades parece un componente de relleno más que una
  tarifa cotizada. Falabella y Despegar, en cambio, no son suma de partes — en el Isleño el
  aéreo implícito de Falabella es de $216 por persona, <b>por debajo del vuelo más barato
  del mercado</b>, lo que indica un descuento real de paquete.</p>
</div>
'''

P_VUELOS = '''
<h2 class="sec">Vuelos, maletas y viajar con niños</h2>
<div class="sec-sub">Rutas y políticas verificadas con búsqueda web el 31/08/2026 · confianza media · precios de extras dinámicos, no verificados al centavo</div>

<p class="lead">La tabla de aéreos del informe compara <b>tarifas base</b>. Para una familia
esa cifra es ficción: en las seis aerolíneas comparadas, <b>ninguna incluye maleta de
bodega</b> en la tarifa que alimenta los comparadores.</p>

<table>
  <tr><th>Aerolínea</th><th>Modelo</th><th>Qué incluye la tarifa base</th><th>Extra familia 4 pax</th></tr>
  <tr><td>LATAM</td><td>Híbrido</td><td>Solo artículo personal · asiento aleatorio</td><td>$120–400</td></tr>
  <tr><td>Avianca</td><td>Híbrido</td><td>Personal + carry-on 10 kg (desde ene-2026)</td><td>$250–700</td></tr>
  <tr><td>Copa</td><td>Full service</td><td>Personal + carry-on 10 kg</td><td>$200–500</td></tr>
  <tr><td>SKY</td><td>Low cost</td><td>Solo un bolso de mano</td><td>$150–350</td></tr>
  <tr><td>JetSmart</td><td>Ultra low cost</td><td>Solo mochila bajo el asiento</td><td>$190–400</td></tr>
  <tr><td>Arajet</td><td>Ultra low cost</td><td>Solo personal 6 kg</td><td>$220–480</td></tr>
</table>
<p class="tcap">«Extra familia» = estimado ida y vuelta para 2 adultos + 2 niños con 2–3 maletas de bodega y asientos juntos, comprando online al reservar. Rangos de fuentes oficiales y prensa especializada; los operadores usan precio dinámico. Comprado en aeropuerto, todos los rangos se duplican.</p>

<div class="caja ambar">
  <h4>Lo que esto le hace a la comparación del informe</h4>
  <p>El vuelo «más barato» de cada ruta deja de serlo cuando se agregan maletas. Una familia
  que elige JetSmart a San Andrés ($591 pp) porque parece más barato que Avianca ($535 pp)
  ya estaba equivocada; al sumar $190–400 de extras, la distancia contra LATAM ($384 pp) se
  vuelve decisiva. <b>El ranking de «mejor aerolínea por ruta» del informe es correcto para
  dos adultos sin equipaje y engañoso para una familia.</b></p>
</div>

'''
P_ESCALAS = '''
<h2 class="sec">Escalas, horarios y traslados</h2>
<div class="sec-sub">Ningún destino del informe tiene vuelo directo desde Santiago, salvo uno</div>
<table>
  <tr><th>Ruta</th><th>Directo</th><th>Mejor opción</th><th>Duración</th><th>Lectura familiar</th></tr>
  <tr><td>SCL → PTY Panamá</td><td class="bien">Sí</td><td>Copa / Avianca</td><td>~7 h</td><td class="bien">La mejor con niños</td></tr>
  <tr><td>SCL → ADZ San Andrés</td><td class="mal">No</td><td>LATAM vía Bogotá</td><td>~11 h</td><td>1 escala, diurno, manejable</td></tr>
  <tr><td>SCL → CTG Cartagena</td><td class="mal">No*</td><td>LATAM vía Bogotá</td><td>~9,5–10 h</td><td>1 escala, diurno</td></tr>
  <tr><td>SCL → SMR Santa Marta</td><td class="mal">No</td><td>JetSmart / LATAM</td><td>~11 h+</td><td class="mal">Riesgo de nocturno</td></tr>
</table>
<p class="tcap">* El directo de Avianca a Cartagena (AV132, 6h40) es estacional: opera solo enero–febrero, no en octubre.</p>

<div class="caja ok">
  <h4>Panamá es nuestro mejor activo logístico y no lo estamos usando</h4>
  <p>Es el <b>único destino del informe con vuelo directo desde Santiago</b>: ~7 horas, sin
  escalas, sin riesgo de conexión perdida. Para una familia con niños o para una pareja que
  quiere que el descanso empiece en el aeropuerto, eso vale más que $100 de diferencia de
  tarifa. Y es justamente el destino donde nuestro hotel tiene el puntaje más bajo de su
  tabla y el Riu está a $96. <b>El activo está; el producto no lo acompaña.</b></p>
</div>

<h3 class="blk">Un dato de traslado que la góndola no comunica</h3>
<p>San Andrés es una isla de 13 km: ningún Decameron está a más de 25 minutos del
aeropuerto, y el Isleño está a <b>1 km</b>. El Galeón queda a 10–15 min del aeropuerto de
Santa Marta. Contra los ~2 horas de carretera hasta Playa Blanca en Panamá o la lancha a
Barú, después de once horas de viaje con niños eso es una ventaja concreta —<b>y no aparece
en ninguna ficha</b>.</p>
'''

P_CLIENTE = '''
<h2 class="sec">Lo que pasa cuando el cliente googlea</h2>
<div class="sec-sub">Dos simulaciones de decisión de compra sobre los datos reales del informe · ejercicio analítico, no investigación de mercado</div>

<p class="lead">El informe compara precios entre operadores. El cliente no: compara
<b>destinos, puntajes y fotos</b>, y decide en el momento en que abre otra pestaña para
buscar el nombre del hotel. Estas dos simulaciones recorren esa decisión con los datos
reales de las tablas.</p>

<div class="persona">
  <div class="ph">Papá, 41 años, hijos de 6 y 11<span>Presupuesto USD 3.000–3.500 por los cuatro · prioriza que los niños estén bien y no trasnochar</span></div>
  <div class="pb">
    <p><b>Elige:</b> San Andrés, Decameron San Luis, en paquete, LATAM diurno vía Bogotá.
    Razona que es el único destino donde el aéreo por cuatro baja de $1.600, que una sola
    escala es el máximo riesgo aceptable con niños, y que el todo incluido real le fija el
    gasto. Descarta el «ahorro» de armarlo por separado porque está calculado con tarifa
    Basic sin maletas.</p>
    <p><b>Dónde casi lo perdemos:</b> al googlear, cuatro de los cinco hoteles de la isla
    marcan 3,0 en TripAdvisor con miles de reseñas que repiten «habitaciones viejas» y «wifi
    malo». Y en ningún momento la góndola le muestra el <b>precio total para cuatro
    personas</b> ni la política de niños: tiene que cotizar aparte justo cuando iba a pagar.</p>
  </div>
  <div class="veredicto"><b>Compra Decameron</b> — gana el precio de entrada, el destino y la escala única. Pero la decisión se sostiene <i>a pesar</i> de la reputación, no gracias a ella.</div>
</div>

<div class="persona">
  <div class="ph">Pareja sin hijos, 30–45 años<span>Presupuesto USD 2.000–2.800 · prioriza descansar y comer bien · compara puntajes antes de pagar</span></div>
  <div class="pb">
    <p><b>Elige:</b> Panamá, <b>Riu Playa Blanca</b>, armado por separado. Copa directo
    ($650 pp, diurno) + hotel $1,059 ≈ $2,359. Es el único combo que cumple sus dos
    prioridades a la vez: cero escalas y el mejor puntaje de la comparación.</p>
    <p><b>Por qué nos deja:</b> por <b>$96 en toda la estadía</b> —menos de $20 por noche—
    cambia un 7,6 masivo por un 8,4 de 5 estrellas. A esa distancia la reputación decide
    sola. Y no encuentra ningún producto para pareja sin niños: toda la nómina está diseñada
    para familias.</p>
  </div>
  <div class="veredicto"><b>No compra Decameron</b> — y en su plan B, San Andrés, su plata igual se iría al Grand Sirenis, el único 5 estrellas de la isla que no es nuestro.</div>
</div>

<div class="caja">
  <h4>Lo que las dos decisiones tienen en común</h4>
  <p>Ninguna de las dos se pierde por precio de tarifa. Se ganan o se pierden en
  <b>reputación pública</b>, en <b>ausencia de información</b> (precio familiar, política de
  niños, qué incluye el paquete) y en <b>coherencia de la oferta</b>. Son tres cosas que se
  arreglan sin tocar la tarifa.</p>
</div>
'''

P_ERRORES = '''
<h2 class="sec">Antes de emitir: qué revisar</h2>
<div class="sec-sub">Ordenado por consecuencia si llega mal a la góndola o a gerencia</div>

<div class="caja alerta">
  <h4>1 · «Grand Decameron Complex» está comparado contra vuelos a Cancún</h4>
  <p>Según el levantamiento, ese hotel está en <b>Bucerías, Riviera Nayarit</b>, a ~20
  minutos del aeropuerto de <b>Puerto Vallarta (PVR)</b>, y Decameron no tendría hotel
  propio en Cancún. El informe usa la ruta <b>SCL → CUN</b> para el bloque México, y Los
  Cabos (SJD) directamente no tiene ruta en la tabla de aéreos.</p>
  <p><b>Si se confirma, invalida el componente aéreo de todo el bloque México</b> —incluido
  el cálculo de paquete contra armar por separado del Complex. Es el punto que revisaría
  primero. <b>No está verificado adversarialmente</b> (esa pasada no alcanzó a correr), pero
  aparece consistentemente en tres fuentes distintas del levantamiento.</p>
</div>

<div class="caja ambar">
  <h4>2 · El $956 de Panamá atribuido al canal directo no tiene respaldo</h4>
  <p>En la tabla de verificación, Panamá es el único hotel con cifra en la columna del
  10–15, y ese número <b>coincide exactamente</b> con lo que la celda de Cocha traía antes
  de corregirse. El archivo de control no incluye Panamá, así que no hay de dónde
  verificarlo: es posible que se haya arrastrado de una celda a la otra. Recotizar antes de
  emitir.</p>
</div>

<div class="caja">
  <h4>3 · Pendientes que ya venían del contraste entre versiones</h4>
  <p><b>Cartagena:</b> Dubai pasó de $1,156 a $587 entre versiones y La Gran Vía de «sin
  disponibilidad» a ser el más barato. Con lo que ahora sabemos —que ambos son hoteles
  urbanos de 3–4 estrellas— conviene reconfirmar no solo el precio sino <b>el régimen</b>:
  si no son todo incluido, no pertenecen a esa tabla.</p>
  <p><b>Barú:</b> la recotización del 31/08 dio $2,142 en alojamiento contra $1,928
  publicado. Falta confirmar el periodo de esa captura antes de corregir la celda. Y sigue
  abierto con qué destino queda: hoy aparece solo en el benchmark, no en la tabla de
  Cartagena.</p>
  <p><b>Panamá, doble carga:</b> la segunda carga sigue sin tarifa en Cocha y Expedia. El
  informe ya no afirma de quién es cada carga —la inferencia por precio nunca se verificó
  con el operador— pero conviene cerrarlo.</p>
  <p><b>Vigencia general:</b> las tarifas de las tablas se cotizaron el 26/08. En cinco días
  Barú se movió $214 en alojamiento y $469 en paquetería. Conviene refrescar antes de
  emitir, o declarar la fecha de cotización con más énfasis.</p>
</div>

<h3 class="blk">Lo que este análisis NO pudo verificar</h3>
<ul>
  <li>Las <b>dos pasadas de verificación adversarial</b> sobre rutas y reputación no
    alcanzaron a ejecutarse. El contraste se hizo a mano contra las tablas del informe, y
    así se descartó al menos una afirmación falsa antes de llegar a este documento.</li>
  <li>Los <b>precios de equipaje y asientos</b> son rangos: todas las aerolíneas usan precio
    dinámico y ninguna publica tabla fija para SCL en octubre de 2026.</li>
  <li>Los <b>puntajes de Google y TripAdvisor</b> de varios hoteles no se pudieron confirmar
    directamente (páginas bloqueadas); donde eso pasó, la tabla lo dice.</li>
  <li>Las <b>categorías por estrellas</b> en Colombia no son oficiales —la clasificación no
    es obligatoria— por eso varían entre plataformas y se reportan como rango.</li>
  <li>Las <b>dos simulaciones de decisión</b> son un ejercicio analítico sobre datos reales,
    no investigación de mercado con clientes.</li>
</ul>
'''

P_RECOM = '''
<h2 class="sec">Qué haría, en orden</h2>
<div class="sec-sub">Priorizado por relación entre impacto y esfuerzo</div>

<ol class="rec">
  <li><b>Levantar con Cocha el problema de exhibición</b>
    Panamá y el Galeón tienen cupo y tarifa y no aparecen en la búsqueda de destino. Es lo
    único de esta lista donde no vendemos <i>a ningún precio</i>. Son dos fichas concretas,
    no un problema del canal completo: Cartagena y Punta Sal se revisaron igual y ahí el NA
    es legítimo, y en San Andrés y México la exhibición funciona bien.</li>
  <li><b>Revisar la carga propia en Expedia</b>
    +23,5% en hoteles propios contra +0,2% en la competencia de las mismas tablas. El
    desvío es nuestro, no del canal. Tres casos de +45% a +64% sirven de evidencia para
    abrir la conversación.</li>
  <li><b>Corregir los paquetes que pierden contra armarlo a mano</b>
    Galeón +$1,028 y Complex +$522 son anti-venta: quien descubre una fila así deja de creer
    en el precio empaquetado de la marca completa. El paquete debe ganar siempre, aunque sea
    por poco, y decir qué incluye que el DIY no (maletas, traslado, asistencia).</li>
  <li><b>Reponer el inventario en NA</b>
    Decameron Cartagena y Punta Sal no se pueden comprar en ninguno de los cuatro
    operadores, y su falta de cupo ya está verificada hotel por hotel. Punta Sal es el caso
    más claro: del 3 al 8 de octubre <b>sí se vende</b> —Despegar lo cotiza en $1,593— pero
    V. Falabella no lo tiene ni en esas fechas. Donde no haya cupo, mostrar fechas
    alternativas en vez de un NA seco: el cliente que ve NA no vuelve, se va a la fila
    siguiente.</li>
  <li><b>Definir la paridad Falabella–Despegar y la brecha de Cocha</b>
    Confirmar si la identidad total entre las dos primeras es intencional, y si el ~11% de
    ventaja de Cocha responde a condiciones pactadas o a un desvío de carga. Hoy nadie en el
    informe puede responderlo.</li>
</ol>
'''
P_RECOM2 = '''
<h2 class="sec">Qué haría, en orden <span style="font-size:9pt;color:#878787">· continuación</span></h2>
<div class="sec-sub">Reputación, producto y presentación en la góndola</div>
<ol class="rec" start="6" style="counter-reset:r 5">
  <li><b>Trabajar la reputación donde se decide la compra</b>
    Subir de 7,0–7,6 hacia 8+ en Booking vale más que cualquier ajuste de tarifa de esta
    lista: en Panamá perdemos por $96 contra un 8,4. Empezar por responder reseñas y
    actualizar fotos de habitaciones, que es lo que el cliente mira antes de pagar.</li>
  <li><b>Destacar a Maryland</b>
    Es el mejor calificado de San Andrés (Google 4,4 · TripAdvisor 4,0 · #3 de 84) y cuesta
    menos que el Isleño, que puntúa 3,0. Es la carta reputacional que tenemos y no está
    puesta adelante.</li>
  <li><b>Empaquetar el vuelo bueno, no el barato</b>
    Para familias, LATAM diurno con maleta incluida como default del paquete, aunque cueste
    más que la tarifa Basic. Es lo que un padre elegiría solo; si el paquete ya lo trae,
    deja de comparar. Y en Panamá, vender el directo de Copa como «sin escalas» —es el único
    argumento logístico que le gana al Riu.</li>
  <li><b>Mostrar precio para familia en la ficha</b>
    Selector con edades, política de niños explícita y total de una vez. Hoy toda la góndola
    cotiza dos adultos y obliga a cotizar aparte justo en el momento de pagar.</li>
  <li><b>Revisar el set de comparables de Cartagena</b>
    Dos de los tres competidores son hoteles urbanos de 3 estrellas. Comparar un todo
    incluido de playa contra eso no informa bien la decisión de tarifa.</li>
</ol>

<div class="caja ok">
  <h4>Lo que este informe confirma que estamos haciendo bien</h4>
  <p><b>San Andrés es una fortaleza estructural</b>: cinco hoteles, pase cruzado entre
  propiedades que ningún competidor puede igualar, la ruta aérea más barata del Caribe desde
  Santiago y el precio de entrada más bajo del segmento ($852 en San Luis). Quien busca todo
  incluido familiar en la isla llega a nosotros por defecto.</p>
  <p><b>Y cuando el paquete está bien armado, convierte</b>: Isleño −$161 y Los Delfines
  −$78 contra armarlo a mano. La promesa de «todo resuelto en un clic» funciona; el problema
  no es el formato, son las tres filas donde el precio se descuadró.</p>
</div>
'''

def html():
    paginas = [PORTADA,
      page(P_CANAL,    'Lectura de canal',        2),
      page(P_COCHA,    'Exhibición en Cocha',     3),
      page(P_ESTRELLAS,'Categoría y reputación',  4),
      page(P_MATIZ,    'Categoría y reputación',  5),
      page(P_VALOR,    'Precio contra producto',  6),
      page(P_PAQUETE,  'Paquete contra armarlo',  7),
      page(P_VUELOS,   'Vuelos y familia',        8),
      page(P_ESCALAS,  'Escalas y traslados',     9),
      page(P_CLIENTE,  'La decisión del cliente',10),
      page(P_ERRORES,  'Revisión previa',        11),
      page(P_RECOM,    'Recomendaciones',        12),
      page(P_RECOM2,   'Recomendaciones',        13),
    ]
    return ('<!doctype html><html><head><meta charset="utf-8"><style>' + CSS +
            '</style></head><body>' + '\n'.join(paginas) + '</body></html>')

def emitir():
    base = 'Analisis_y_Opiniones_Competencia_10-15_Oct_2026'
    hf = os.path.join(AQUI, base + '.html')
    pf = os.path.join(AQUI, base + '.pdf')
    with open(hf, 'w', encoding='utf-8') as f:
        f.write(html())
    subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu',
        '--no-pdf-header-footer', f'--print-to-pdf={pf}', 'file://' + hf],
        capture_output=True, text=True, timeout=120)
    ok = os.path.exists(pf) and os.path.getsize(pf) > 10000
    print(base + '.pdf', 'OK' if ok else 'FALLO', os.path.getsize(pf) if ok else '')
    return pf

if __name__ == '__main__':
    emitir()
