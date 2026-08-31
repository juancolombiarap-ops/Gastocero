# -*- coding: utf-8 -*-
"""Emite el Reporte de Competencia 10-15 Oct 2026 V.3 en PDF, formato de referencia.

Reproduce la estructura del V.2 que entregó Juan (portada con degradé y logo,
tablas por destino, benchmark, aéreos y resúmenes) con los datos corregidos el
31/08/2026, en dos versiones:

  - INTERNA:  con las verificaciones del canal directo (decameronchile.cl).
  - COLOMBIA: sin ninguna mención del canal directo ni de decameron.com.
              Las referencias que sí lleva son de los operadores (OTA).

Correcciones aplicadas sobre el V.2:
  * Panamá alojamiento, Cocha: 956 -> 963 (recotizado por hotel y fecha; el
    hotel no aparece en la búsqueda de destino de Cocha).
  * Galeón alojamiento: NA -> 1.461 en Cocha (mismo caso de exhibición); pasa
    a ser el más económico de su tabla y se cierra la contradicción con su
    propio paquete.
  * Cargas dobles de Panamá: se publica solo la más baja y no se afirma el
    origen de cada carga (la inferencia por precio no está verificada).
  * Benchmark paquetería: Barú en V. Falabella 2.559 -> 3.028 (confirmado);
    el MEJOR de esa fila pasa a Cocha 2.605.
  * Cartagena paquetería: se agrega la fila NA de Decameron Cartagena.
  * Celdas NA con referencia del 3-8 oct al pie (regla del informe).

Uso:  python3 emitir_pdf.py            -> genera ambos PDF
"""
import base64, os, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
CHROME = '/opt/pw-browsers/chromium'

def b64(path, mime):
    with open(os.path.join(AQUI, path), 'rb') as f:
        return f'data:{mime};base64,' + base64.b64encode(f.read()).decode()

LOGO = b64('marca/logo_decameron.png', 'image/png')
GRAD = b64('marca/portada_gradiente.jpg', 'image/jpeg')

# ---------------------------------------------------------------------------
# DATOS (V.2 con las correcciones del 31/08)
# ---------------------------------------------------------------------------
# fila: (tipo, hotel, [fal, des, coc, exp])  — 'NA'/'N/D' como texto
ALOJ = [
 ('SAN ANDRÉS', 'ADZ', [
   ('D','DECAMERON ISLEÑO',        [1642,1642,1467,2687]),
   ('D','DECAMERON SAN LUIS',      [954,954,852,1046]),
   ('D','DECAMERON MARAZUL',       [1066,1066,951,1748]),
   ('D','DECAMERON MARYLAND',      [1246,1246,1114,1810]),
   ('D','DECAMERON LOS DELFINES',  [1344,1344,1196,1515]),
   ('C','SOL CARIBE SAN ANDRES',   [1476,1476,1138,1500]),
   ('C','SOL CARIBE CAMPO',        [1636,1636,1138,'NA']),
   ('C','EL DORADO',               [2272,2272,'NA',1683]),
   ('C','GRAND SIRENIS SAN ANDRÉS',[2248,2248,1942,2274]),
  ], []),
 ('CARTAGENA', 'CTG', [
   ('D','DECAMERON CARTAGENA',     ['NA','NA','NA','NA']),
   ('C','DORADO PLAZA BOCAGRANDE', [1132,1132,967,1162]),
   ('C','HOTEL DUBAI CARTAGENA',   [587,587,588,628]),
   ('C','HOTEL LA GRAN VÍA',       [580,580,'NA','NA']),
  ], ['nota_ctg_aloj']),
 ('PUNTA SAL', 'TBP', [
   ('D','ROYAL DECAMERON PUNTA SAL',['NA','NA','NA','NA']),
  ], ['nota_zona_tbp','nota_tbp_aloj']),
 ('PANAMÁ', 'PTY', [
   ('D','GRAND DECAMERON PANAMÁ',  [1008,1008,963,1213]),
   ('C','RIU PLAYA BLANCA ALL INCLUSIVE',[1110,1110,1087,1059]),
   ('C','GRAN EVENIA BIJAO',       [810,810,788,956]),
   ('C','DREAMS PLAYA BONITA PANAMA',[1367,1367,1207,1392]),
  ], ['nota_pty_dobles_aloj','nota_pty_cocha','nota_pty_ref']),
 ('SANTA MARTA', 'SMR', [
   ('D','DECAMERON GALEÓN',        ['NA','NA',1461,'NA']),
   ('C','HOTEL PORTO HORIZONTE',   [1758,1758,'NA',1756]),
  ], ['nota_smr_corregida','nota_smr_irotama']),
 ('MÉXICO', 'MEX', [
   ('D','GRAND DECAMERON COMPLEX', [1304,1304,1163,1357]),
   ('D','GRAND DECAMERON LOS CABOS',[2174,2174,1479,1479]),
  ], []),
]

PAQ = [
 ('SAN ANDRÉS', 'ADZ', [
   ('D','DECAMERON ISLEÑO',        [2074,2229,2316,3117]),
   ('D','DECAMERON SAN LUIS',      [1697,1807,1701,2191]),
   ('D','DECAMERON MARAZUL',       [1737,1848,1801,2726]),
   ('D','DECAMERON MARYLAND',      [1894,2035,1963,2508]),
   ('D','DECAMERON LOS DELFINES',  [1886,2065,2046,2311]),
   ('C','SOL CARIBE SAN ANDRES',   [1952,2174,1967,2236]),
   ('C','SOL CARIBE CAMPO',        [1952,2174,1967,'NA']),
   ('C','EL DORADO',               ['NA','NA','NA',2481]),
   ('C','GRAND SIRENIS SAN ANDRÉS',[2448,2718,2713,2882]),
  ], []),
 ('CARTAGENA', 'CTG', [
   ('D','DECAMERON CARTAGENA',     ['NA','NA','NA','NA']),
   ('C','DORADO PLAZA BOCAGRANDE', [1960,1954,1976,'N/D']),
   ('C','HOTEL DUBAI CARTAGENA',   [1615,1564,'NA','N/D']),
   ('C','HOTEL LA GRAN VÍA',       [1574,1542,'NA','N/D']),
  ], ['nota_ctg_paq']),
 ('PUNTA SAL', 'TBP', [
   ('D','ROYAL DECAMERON PUNTA SAL',['NA','NA','NA','NA']),
  ], ['nota_zona_tbp','nota_tbp_paq']),
 ('PANAMÁ', 'PTY', [
   ('D','GRAND DECAMERON PANAMÁ',  [2514,2588,2273,'N/D']),
   ('C','RIU PLAYA BLANCA ALL INCLUSIVE',[2576,2650,2366,'N/D']),
   ('C','GRAN EVENIA BIJAO',       [2346,2438,2105,'N/D']),
   ('C','DREAMS PLAYA BONITA PANAMA',[2772,2863,2496,'N/D']),
  ], ['nota_pty_dobles_paq','nota_pty_expedia','nota_pty_ref_paq']),
 ('SANTA MARTA', 'SMR', [
   ('D','DECAMERON GALEÓN',        ['NA','NA',3357,'NA']),
   ('C','HOTEL PORTO HORIZONTE',   [2267,3163,2459,2610]),
  ], ['nota_smr_paq','nota_smr_irotama']),
 ('MÉXICO', 'MEX', [
   ('D','GRAND DECAMERON COMPLEX', ['NA','NA',3097,3364]),
   ('D','GRAND DECAMERON LOS CABOS',[3946,4306,3108,3155]),
  ], []),
]

# benchmark: (categoria, hotel, dest, [fal,des,coc,exp], vs_texto)
BENCH_ALOJ = [
 ('DECAMERON','DECAMERON ISLEÑO','ADZ',[1642,1642,1467,2687],'REF'),
 ('DECAMERON','DECAMERON BARÚ','CTG',[2142,1928,1712,2440],'—'),
 ('PUNTA CANA','BARCELO BAVARO PALACE','PUJ',[1126,1126,1102,1143],'Isleño +33%'),
 ('PUNTA CANA','SERENADE CARIBE CLUB FAMILY','PUJ',[1222,1222,1002,1221],'Isleño +46%'),
 ('PUNTA CANA','GRAND SIRENIS PUNTA CANA','PUJ',[1304,1304,891,1304],'Isleño +65%'),
 ('PUNTA CANA','VIK HOTEL CAYENA','PUJ',[1424,1424,1204,1422],'Isleño +22%'),
 ('CANCÚN','RIU DUNAMAR','CUN',[1046,'NA',1004,1197],'Isleño +46%'),
 ('CANCÚN','FLAMINGO CANCUN','CUN',[1090,1090,1004,1202],'Isleño +46%'),
 ('CANCÚN','SUNSET MARINA RESORT','CUN',[958,958,859,1293],'Isleño +71%'),
 ('CANCÚN','DREAMS RIVIERA','CUN',['NA','NA',1204,1377],'Isleño +22%'),
 ('CANCÚN','HYATT VIVID CANCUN','CUN',[1426,1426,'NA',1429],'Isleño +3%'),
 ('CURAZAO','ZOËTRY CURAÇAO RESORT & SPA','CUR',[2784,2784,2266,2780],'Isleño −35%'),
 ('CURAZAO','MANGROVE BEACH CORENDON CURAÇAO','CUR',[2004,2004,1831,2004],'Isleño −20%'),
 ('CURAZAO','DREAMS CURACAO','CUR',[2238,2238,1864,2237],'Isleño −21%'),
]
BENCH_PAQ = [
 ('DECAMERON','DECAMERON ISLEÑO','ADZ',[2074,2229,2316,3117],'REF'),
 ('DECAMERON','DECAMERON BARÚ','CTG',[3028,2636,2605,3479],'—'),   # 2559 -> 3028 confirmado
 ('PUNTA CANA','BARCELO BAVARO PALACE','PUJ',[2296,2393,2327,2329],'Isleño −10%'),
 ('PUNTA CANA','SERENADE CARIBE CLUB FAMILY','PUJ',[2232,2391,2351,2413],'Isleño −7%'),
 ('PUNTA CANA','GRAND SIRENIS PUNTA CANA','PUJ',[2119,2282,2218,2681],'Isleño −2%'),
 ('PUNTA CANA','VIK HOTEL CAYENA','PUJ',[2475,2596,'NA','NA'],'Isleño −16%'),
 ('CANCÚN','RIU DUNAMAR','CUN',[2371,2512,2349,2503],'Isleño −12%'),
 ('CANCÚN','FLAMINGO CANCUN','CUN',[2400,2609,2375,2317],'Isleño −10%'),
 ('CANCÚN','SUNSET MARINA RESORT','CUN',[2274,2500,2225,2332],'Isleño −7%'),
 ('CANCÚN','DREAMS RIVIERA','CUN',['NA','NA','NA',2714],'Isleño −24%'),
 ('CANCÚN','HYATT VIVID CANCUN','CUN',[2666,2890,'NA',2817],'Isleño −22%'),
 ('CURAZAO','ZOËTRY CURAÇAO RESORT & SPA','CUR',[3653,3913,3490,3767],'Isleño −41%'),
 ('CURAZAO','MANGROVE BEACH CORENDON CURAÇAO','CUR',['NA','NA',3042,3029],'Isleño −32%'),
 ('CURAZAO','DREAMS CURACAO','CUR',['NA','NA',3095,3248],'Isleño −33%'),
]

AEREOS = [  # ruta, [latam, avianca, copa, sky, jetsmart, arajet]
 ('SCL → ADZ',[384,535,744,'NA',591,'NA']),
 ('SCL → CTG',[404,569,1006,'NA',430,'NA']),
 ('SCL → TBP',[422,'NA','NA',567,'NA','NA']),
 ('SCL → PUJ',[667,715,858,846,'NA',606]),
 ('SCL → CUN',[706,872,720,'NA','NA',772]),
 ('SCL → SMR',[507,742,600,'NA',434,'NA']),
 ('SCL → PTY',['NA',580,650,'NA','NA','NA']),
]

MEJOR_OP = [  # hotel, mejor op, precio, 2do, precio2, dif
 ('DECAMERON ISLEÑO','COCHA',1467,'DESPEGAR',1642,'−11%'),
 ('DECAMERON SAN LUIS','COCHA',852,'DESPEGAR',954,'−11%'),
 ('DECAMERON MARAZUL','COCHA',951,'DESPEGAR',1066,'−11%'),
 ('DECAMERON MARYLAND','COCHA',1114,'DESPEGAR',1246,'−11%'),
 ('DECAMERON LOS DELFINES','COCHA',1196,'DESPEGAR',1344,'−11%'),
 ('DECAMERON BARÚ','COCHA',1712,'DESPEGAR',1928,'−11%'),
 ('GRAND DECAMERON PANAMÁ','COCHA',963,'V. FALABELLA',1008,'−4%'),
 ('DECAMERON GALEÓN','COCHA',1461,'único canal con tarifa','','—'),
 ('GRAND DECAMERON COMPLEX','COCHA',1163,'DESPEGAR',1304,'−11%'),
 ('GRAND DECAMERON LOS CABOS','COCHA',1479,'EXPEDIA',1479,'0%'),
]

BENCH_RESUMEN = [
 ('SUNSET MARINA RESORT','CANCÚN',859,'−$608','Isleño +71%'),
 ('GRAND SIRENIS PUNTA CANA','PUNTA CANA',891,'−$576','Isleño +65%'),
 ('SERENADE CARIBE CLUB FAMILY','PUNTA CANA',1002,'−$465','Isleño +46%'),
 ('RIU DUNAMAR','CANCÚN',1004,'−$463','Isleño +46%'),
 ('FLAMINGO CANCUN','CANCÚN',1004,'−$463','Isleño +46%'),
]

MEJOR_AER = [
 ('SCL-ADZ','LATAM',384,'AVIANCA',535,'+39%'),
 ('SCL-CTG','LATAM',404,'JETSMART',430,'+6%'),
 ('SCL-TBP','LATAM',422,'SKY',567,'+34%'),
 ('SCL-PUJ','ARAJET',606,'LATAM',667,'+10%'),
 ('SCL-CUN','LATAM',706,'COPA',720,'+2%'),
 ('SCL-SMR','JETSMART',434,'LATAM',507,'+17%'),
 ('SCL-PTY','AVIANCA',580,'COPA',650,'+12%'),
]

# ---------------------------------------------------------------------------
# NOTAS AL PIE — por versión
# ---------------------------------------------------------------------------
def notas(version):
    interna = version == 'interna'
    n = {
     'nota_zona_tbp': ('Sin oferta All Inclusive comparable en la zona; el contraste se '
        'realiza entre operadores sobre el mismo producto Decameron.'),
     'nota_ctg_aloj': ('Sin disponibilidad en ningún canal para estas fechas: CARTAGENA PLAZA '
        '(Expedia exige mínimo 7 noches). DECAMERON CARTAGENA figura NA en los cuatro '
        'operadores. VALOR REFERENCIAL del 3 al 8 de octubre: V. Falabella lo cotiza en '
        'US$ 1,136 (tarifa promocional −35%, impuestos incluidos).'
        + (' También está sin cupo en la venta web directa; del 3 al 8 el canal directo '
           '(decameronchile.cl) lo cotiza en habitación Estándar US$ 979 No Reembolsable y '
           'US$ 1,085 Flex. Cotizado el 31/08/2026.' if interna else '')),
     'nota_tbp_aloj': ('ROYAL DECAMERON PUNTA SAL figura NA porque está sin cupo para estas '
        'fechas en los cuatro operadores. VALOR REFERENCIAL del 3 al 8 de octubre: Despegar '
        'sí lo vende, en US$ 1,593 por la estadía (All Inclusive, impuestos incluidos, 5 '
        'noches y 2 personas). V. Falabella, en cambio, también sale sin disponibilidad para '
        'esas fechas: de los operadores consultados, Despegar es el único con tarifa.'
        + (' En la venta web directa está igualmente sin cupo; del 3 al 8 el canal directo '
           'lo vende en US$ 1,524 (Superior Plus, única categoría publicada, sin rótulo de '
           'modalidad). Cotizado el 31/08/2026.' if interna else '')),
     'nota_pty_dobles_aloj': ('El operador tiene este hotel cargado dos veces con tarifas '
        'distintas. Se publica la más baja; la otra quedaba en $1,177. El origen de cada '
        'carga no está verificado con el operador, por eso no se rotula.'),
     'nota_pty_cocha': ('Celda de Cocha recotizada el 31/08/2026 entrando por hotel y fecha: '
        '$963 (habitación estándar con vista al jardín, cancelación gratuita hasta el 6 de '
        'octubre). El hotel NO aparece en la búsqueda de destino de Cocha, ni en alojamiento '
        'ni en paquetería: la tarifa solo se encuentra buscando el hotel directamente.'),
     'nota_pty_ref': ('VALOR REFERENCIAL del 3 al 8 de octubre: V. Falabella cotiza el hotel '
        'en US$ 1,480 (alojamiento, All Inclusive).'
        + (' El canal directo lo cotiza en US$ 875 (Garden View: no publica Standard en esas '
           'fechas, se declara la categoría). Cotizado el 31/08/2026.' if interna else '')),
     'nota_smr_corregida': ('Celda de Cocha REHECHA el 31/08/2026 entrando por hotel y fecha: '
        'US$ 1,461 en habitación Estándar, todo incluido, sin cambio ni devolución (la misma '
        'Estándar con cancelación gratuita hasta el 29/09: US$ 1,624). El NA anterior no era '
        'falta de cupo: el hotel no aparece en la búsqueda de destino de Cocha. V. Falabella, '
        'Despegar y Expedia siguen sin tarifa; VALOR REFERENCIAL del 3 al 8: V. Falabella '
        'US$ 1,682 y Despegar US$ 1,660, ambas con aviso «Solo queda 1» (tarifa de última '
        'habitación).'),
     'nota_smr_irotama': ('Sin disponibilidad en ningún canal para estas fechas: IROTAMA DEL SOL.'),
     'nota_ctg_paq': ('DECAMERON CARTAGENA y CARTAGENA PLAZA sin disponibilidad en ningún '
        'canal para estas fechas. Del 3 al 8 de octubre V. Falabella también cotiza el '
        'paquete del Decameron Cartagena sin disponibilidad (NA).'),
     'nota_tbp_paq': ('ROYAL DECAMERON PUNTA SAL figura sin disponibilidad en los cuatro '
        'operadores; del 3 al 8 de octubre también aparece sin cupo en V. Falabella. La '
        'referencia de Despegar para esas fechas (US$ 1,593) es solo alojamiento y no es '
        'comparable con esta tabla: la columna de paquetería es el paquete que arma el '
        'operador, otro producto.'
        + (' La referencia de alojamiento del canal directo (US$ 1,524) no es comparable con '
           'esta tabla: la columna de paquetería es el paquete que arma el operador, otro '
           'producto.' if interna else '')),
     'nota_pty_dobles_paq': ('El operador tiene este hotel cargado dos veces; se publica la '
        'más baja y la otra quedaba en $2,756. El origen de cada carga no está verificado, '
        'por eso no se rotula.'),
     'nota_pty_expedia': ('En la re-cotización del 28/08 Expedia bloqueó la consulta '
        'automática; su columna de paquetería queda sin cotizar (N/D).'),
     'nota_pty_ref_paq': ('VALOR REFERENCIAL del 3 al 8 de octubre: V. Falabella cotiza el '
        'paquete (vuelo + alojamiento, impuestos y tasas incluidos) en US$ 2,555 para 2 '
        'personas ($2.409.546 CLP al cambio de $943).'),
     'nota_smr_paq': ('El paquete del Galeón existe solo en Cocha ($3,357). La contradicción '
        'que traía el informe —paquete disponible con alojamiento «sin cupo»— quedó '
        'resuelta: la celda equivocada era la de alojamiento, ya corregida (US$ 1,461). '
        'VALOR REFERENCIAL del 3 al 8: Despegar cotiza el paquete en US$ 2,651 para 2 '
        'personas, vuelo con escalas SCL↔SMR, impuestos incluidos.'),
    }
    return n

LEYENDA = ('▼ Más económico de la tabla&nbsp;&nbsp;|&nbsp;&nbsp;▲ Más caro&nbsp;&nbsp;|'
           '&nbsp;&nbsp;NA = cotizado sin disponibilidad o sin tarifa&nbsp;&nbsp;|&nbsp;&nbsp;'
           'N/D = canal no cotizado para ese hotel')

# ---------------------------------------------------------------------------
# RENDER
# ---------------------------------------------------------------------------
def usd(v):
    return v if isinstance(v,str) else '${:,}'.format(v)

def fila_tabla(tipo, hotel, vals, marca_min=None, marca_max=None):
    nums = [v for v in vals if isinstance(v,int)]
    mejor = min(nums) if nums else None
    tds = []
    for v in vals:
        cls = ' class="na"' if isinstance(v,str) else ''
        tds.append(f'<td{cls}>{usd(v)}</td>')
    if mejor is None:
        mcell = '—'
    else:
        m = usd(mejor)
        if marca_min == hotel: m += ' <span class="abajo">▼</span>'
        if marca_max == hotel: m += ' <span class="arriba">▲</span>'
        mcell = m
    t = 'DECAMERON' if tipo=='D' else 'COMPETENCIA'
    cl = ' class="propio"' if tipo=='D' else ''
    return (f'<tr{cl}><td class="tipo">{t}</td><td class="hotel">{hotel}</td>'
            + ''.join(tds) + f'<td class="mejor">{mcell}</td></tr>')

def tabla_destino(nombre, cod, filas, claves_notas, N):
    # marcas ▼▲ por MEJOR de la tabla
    mejores = {}
    for _,h,vals in filas:
        nums=[v for v in vals if isinstance(v,int)]
        if nums: mejores[h]=min(nums)
    mmin = min(mejores, key=mejores.get) if len(mejores)>1 else None
    mmax = max(mejores, key=mejores.get) if len(mejores)>1 else None
    cuerpo = '\n'.join(fila_tabla(t,h,v,mmin,mmax) for t,h,v in filas)
    notas_html = ''.join(f'<p class="nota">{N[k]}</p>' for k in claves_notas)
    return f'''<div class="bloque">
  <div class="cab"><span class="dest">{nombre}</span><span class="cod">{cod}</span></div>
  <table>
    <thead><tr><th>Tipo</th><th>Hotel</th><th>V. Falabella</th><th>Despegar</th><th>Cocha</th><th>Expedia</th><th>Mejor</th></tr></thead>
    <tbody>{cuerpo}</tbody>
  </table>
  <p class="leyenda">{LEYENDA}</p>
  {notas_html}
</div>'''

def tabla_bench(filas, ref_precio, titulo):
    out=[]
    mejores={}
    for cat,h,dest,vals,vs in filas:
        nums=[v for v in vals if isinstance(v,int)]
        if nums and cat!='DECAMERON': mejores[h]=min(nums)
    mmin=min(mejores,key=mejores.get) if mejores else None
    for cat,h,dest,vals,vs in filas:
        nums=[v for v in vals if isinstance(v,int)]
        mejor=min(nums) if nums else None
        tds=''.join(f'<td{" class=na" if isinstance(v,str) else ""}>{usd(v)}</td>' for v in vals)
        mtxt = usd(mejor) if mejor is not None else '—'
        if vs=='REF': mtxt += ' <span class="ref">★ REF</span>'; vs='—'
        elif h==mmin: mtxt += ' <span class="abajo">▼</span>'
        cl=' class="propio"' if cat=='DECAMERON' else ''
        out.append(f'<tr{cl}><td class="tipo">{cat}</td><td class="hotel">{h}</td><td class="tipo">{dest}</td>{tds}<td class="mejor">{mtxt}</td><td class="vs">{vs}</td></tr>')
    filas_html='\n'.join(out)
    return f'''<div class="bloque">
  <div class="cab"><span class="dest">{titulo}</span><span class="cod">BENCHMARK</span></div>
  <table class="bench">
    <thead><tr><th>Categoría</th><th>Hotel</th><th>Dest</th><th>V. Falabella</th><th>Despegar</th><th>Cocha</th><th>Expedia</th><th>Mejor</th><th>vs Isleño</th></tr></thead>
    <tbody>{filas_html}</tbody>
  </table>
  <p class="leyenda">★ REF = referencia del benchmark (Isleño {usd(ref_precio)}, mejor tarifa OTA)&nbsp;&nbsp;|&nbsp;&nbsp;▼ Competidor más económico&nbsp;&nbsp;|&nbsp;&nbsp;Última columna, base precio del competidor: Isleño +X% = el Isleño está X% más caro que ese hotel; Isleño −X% = está X% más barato. MEJOR considera solo canales OTA.</p>
  <p class="nota">DECAMERON BARÚ, paquetería: celda de V. Falabella corregida el 31/08/2026 de $2,559 a $3,028 (recotización confirmada); con eso el mejor de esa fila pasa a Cocha ($2,605). En alojamiento la recotización del 31/08 dio $2,142 contra los $1,928 publicados; queda pendiente confirmar el periodo de esa captura antes de corregir la celda.</p>
</div>''' if titulo.startswith('PAQ') else f'''<div class="bloque">
  <div class="cab"><span class="dest">{titulo}</span><span class="cod">BENCHMARK</span></div>
  <table class="bench">
    <thead><tr><th>Categoría</th><th>Hotel</th><th>Dest</th><th>V. Falabella</th><th>Despegar</th><th>Cocha</th><th>Expedia</th><th>Mejor</th><th>vs Isleño</th></tr></thead>
    <tbody>{filas_html}</tbody>
  </table>
  <p class="leyenda">★ REF = referencia del benchmark (Isleño {usd(ref_precio)}, mejor tarifa OTA)&nbsp;&nbsp;|&nbsp;&nbsp;▼ Competidor más económico&nbsp;&nbsp;|&nbsp;&nbsp;Última columna, base precio del competidor: Isleño +X% = el Isleño está X% más caro que ese hotel; Isleño −X% = está X% más barato. MEJOR considera solo canales OTA.</p>
  <p class="nota">DECAMERON BARÚ, alojamiento: celda de V. Falabella corregida el 31/08/2026 de $1,928 a <b>$2,142</b> (US$ 2,142 publicados en dólares sobre lista de US$ 3,150, −32%, impuestos incluidos y cancelación gratis; periodo confirmado con el calendario del operador: 10 al 15 de octubre). El MEJOR de la fila no cambia, sigue siendo Cocha con $1,712. <b>Ojo al leer esta fila:</b> la celda de Despegar es de la cotización del 27/08 y la de V. Falabella del 31/08, así que la fila mezcla dos fechas. Esa es la razón de que aquí no coincidan, no una diferencia entre los dos canales.</p>
</div>'''

def tabla_aereos():
    filas=[]
    for ruta, vals in AEREOS:
        nums=[v for v in vals if isinstance(v,int)]
        mn,mx=min(nums),max(nums)
        tds=[]
        for v in vals:
            if isinstance(v,str): tds.append(f'<td class="na">{v}</td>')
            elif v==mn: tds.append(f'<td class="abajo"><b>{usd(v)}</b></td>')
            elif v==mx: tds.append(f'<td class="arriba">{usd(v)}</td>')
            else: tds.append(f'<td>{usd(v)}</td>')
        filas.append(f'<tr><td class="hotel">{ruta}</td>{"".join(tds)}</tr>')
    cuerpo='\n'.join(filas)
    return f'''<div class="bloque">
  <div class="cab"><span class="dest">TARIFAS AÉREAS DESDE SANTIAGO</span><span class="cod">por persona · ida y vuelta · USD</span></div>
  <table>
    <thead><tr><th>Ruta</th><th>Latam</th><th>Avianca</th><th>Copa</th><th>Sky</th><th>JetSmart</th><th>Arajet</th></tr></thead>
    <tbody>{cuerpo}</tbody>
  </table>
  <p class="leyenda"><span class="abajo">Verde</span> = más barato por ruta&nbsp;&nbsp;|&nbsp;&nbsp;<span class="arriba">Rojo</span> = más caro&nbsp;&nbsp;|&nbsp;&nbsp;NA = aerolínea sin vuelo en la ruta</p>
</div>'''

def tabla_resumen(titulo, cab, filas, nota=''):
    ths=''.join(f'<th>{c}</th>' for c in cab)
    trs=''
    for f in filas:
        tds=''.join(f'<td>{usd(x) if isinstance(x,int) else x}</td>' for x in f)
        trs+=f'<tr>{tds}</tr>'
    return f'''<div class="bloque">
  <div class="cab"><span class="dest">{titulo}</span></div>
  <table class="res"><thead><tr>{ths}</tr></thead><tbody>{trs}</tbody></table>
  {f'<p class="leyenda">{nota}</p>' if nota else ''}
</div>'''

def pagina(cuerpo, pie, num):
    return f'''<div class="page">
  <div class="head"><img src="{LOGO}" class="minilogo"><div class="htxt"><b>REPORTE DE COMPETENCIA</b> · Hoteles Decameron Chile · 10 – 15 Octubre 2026 · V.3</div></div>
  {cuerpo}
  <div class="foot"><span>{pie}</span><span>{num}</span></div>
</div>'''

def html(version):
    N = notas(version)
    interna = version=='interna'
    sello = 'VERSIÓN INTERNA' if interna else 'VERSIÓN COLOMBIA'
    metodo_extra = (' DECAMERON CARTAGENA y ROYAL DECAMERON PUNTA SAL verificados también '
                    'sin cupo en la venta web directa (motor de decameronchile.cl).'
                    if interna else '')
    portada = f'''<div class="page portada" style="background-image:url({GRAD})">
  <div class="tarjeta">
    <img src="{LOGO}" class="logo">
    <h1>REPORTE DE COMPETENCIA</h1>
    <h2>HOTELES DECAMERON CHILE</h2>
    <div class="periodo">10 – 15 Octubre 2026</div>
    <div class="canales">CANALES: V. FALABELLA&nbsp;|&nbsp;DESPEGAR&nbsp;|&nbsp;COCHA&nbsp;|&nbsp;EXPEDIA</div>
    <p class="metodo">Análisis comparativo: Alojamiento, Paquetería y Aéreos. Precios en USD, total de
      la estadía para 2 adultos, habitación Standard en todos los operadores (si un hotel no tiene
      Standard disponible se toma la categoría siguiente y se indica en la tabla), tarifa más económica
      de esa categoría, régimen All Inclusive donde aplica. Datos actualizados al 27/08/2026; Cartagena,
      Punta Sal y Panamá re-cotizados el 28/08/2026. En la re-cotización, Expedia bloqueó la consulta
      automática: su columna de alojamiento se obtuvo vía Hoteles.com (mismo grupo e inventario Expedia,
      precios en USD) y su paquetería quedó sin cotizar (N/D). Conversión CLP→USD al tipo de cambio $943.</p>
    <p class="metodo"><b>V.3 — verificación y correcciones del 31/08/2026:</b> Panamá y Galeón recotizados
      en Cocha por hotel y fecha ($963 y $1,461: ambos figuraban NA o desactualizados porque el hotel no
      aparece en la búsqueda de destino de ese operador); Barú corregido en paquetería ($3,028); cargas
      dobles publicadas por su tarifa más baja, sin rotular origen; celdas NA acompañadas de valor
      referencial del 3–8 de octubre.{metodo_extra} Las tarifas se mueven día a día: las cifras son la
      foto de su fecha de cotización.</p>
    <div class="sello">{sello}</div>
  </div>
</div>'''
    A = {n[0]:(n[0],n[1],n[2],n[3]) for n in []}  # placeholder
    def seccion(nombre): return f'<div class="titulo-seccion">{nombre}</div>'
    paginas = [portada]
    # ALOJAMIENTO: San Andrés | CTG+TBP | PTY+SMR | MEX + bench
    d = {x[0]:x for x in ALOJ}
    paginas.append(pagina(seccion('ALOJAMIENTO · 10 – 15 Octubre 2026 · 2 adultos · USD')
        + tabla_destino(*d['SAN ANDRÉS'][0:2], d['SAN ANDRÉS'][2], d['SAN ANDRÉS'][3], N), 'Alojamiento', 2))
    paginas.append(pagina(tabla_destino(*d['CARTAGENA'][0:2], d['CARTAGENA'][2], d['CARTAGENA'][3], N)
        + tabla_destino(*d['PUNTA SAL'][0:2], d['PUNTA SAL'][2], d['PUNTA SAL'][3], N), 'Alojamiento', 3))
    paginas.append(pagina(tabla_destino(*d['PANAMÁ'][0:2], d['PANAMÁ'][2], d['PANAMÁ'][3], N)
        + tabla_destino(*d['SANTA MARTA'][0:2], d['SANTA MARTA'][2], d['SANTA MARTA'][3], N), 'Alojamiento', 4))
    paginas.append(pagina(tabla_destino(*d['MÉXICO'][0:2], d['MÉXICO'][2], d['MÉXICO'][3], N)
        + tabla_bench(BENCH_ALOJ, 1467, 'ALOJAMIENTO — ISLEÑO VS COMPETENCIA INTERNACIONAL'), 'Alojamiento · Benchmark', 5))
    # PAQUETERÍA
    p = {x[0]:x for x in PAQ}
    paginas.append(pagina(seccion('PAQUETERÍA · Hotel + Aéreo · 10 – 15 Octubre 2026 · 2 adultos · USD')
        + tabla_destino(*p['SAN ANDRÉS'][0:2], p['SAN ANDRÉS'][2], p['SAN ANDRÉS'][3], N), 'Paquetería', 6))
    paginas.append(pagina(tabla_destino(*p['CARTAGENA'][0:2], p['CARTAGENA'][2], p['CARTAGENA'][3], N)
        + tabla_destino(*p['PUNTA SAL'][0:2], p['PUNTA SAL'][2], p['PUNTA SAL'][3], N), 'Paquetería', 7))
    paginas.append(pagina(tabla_destino(*p['PANAMÁ'][0:2], p['PANAMÁ'][2], p['PANAMÁ'][3], N)
        + tabla_destino(*p['SANTA MARTA'][0:2], p['SANTA MARTA'][2], p['SANTA MARTA'][3], N), 'Paquetería', 8))
    paginas.append(pagina(tabla_destino(*p['MÉXICO'][0:2], p['MÉXICO'][2], p['MÉXICO'][3], N)
        + tabla_bench(BENCH_PAQ, 2074, 'PAQUETERÍA — ISLEÑO VS COMPETENCIA INTERNACIONAL'), 'Paquetería · Benchmark', 9))
    # AÉREOS + resúmenes
    paginas.append(pagina(tabla_aereos()
        + tabla_resumen('MEJOR OPERADOR POR HOTEL — ALOJAMIENTO',
            ['Hotel','Mejor op.','Precio','2do mejor','Precio','Dif'],
            MEJOR_OP,
            'Panamá corregido a $963 (Cocha, recotizado por hotel y fecha). El Galeón queda con Cocha como único canal con tarifa.'),
        'Aéreos · Resúmenes', 10))
    paginas.append(pagina(
        tabla_resumen('BENCHMARK ISLEÑO (MEJOR TARIFA OTA $1,467) VS COMPETENCIA INTERNACIONAL',
            ['Competidor','Destino','Mejor OTA','vs Isleño','Dif'], BENCH_RESUMEN,
            'DIF con base en el precio del competidor: Isleño +X% = el Isleño está X% más caro que ese hotel.')
        + tabla_resumen('MEJOR AEROLÍNEA POR RUTA',
            ['Ruta','Mejor','Precio','2da opc.','Precio','Dif'], MEJOR_AER),
        'Resúmenes', 11))
    cuerpo = '\n'.join(paginas)
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; margin:0; padding:0; }}
body {{ font-family: 'Segoe UI', 'DejaVu Sans', Arial, sans-serif; color:#16324A; }}
.page {{ width:210mm; height:297mm; padding:12mm 13mm 14mm; page-break-after:always; position:relative; background:#fff; }}
.portada {{ background-size:cover; background-position:center; display:flex; align-items:center; justify-content:center; padding:0; }}
.tarjeta {{ background:rgba(255,255,255,.97); width:158mm; border-radius:4mm; padding:14mm 14mm 12mm; text-align:center; box-shadow:0 4mm 12mm rgba(0,0,0,.25); }}
.logo {{ width:88mm; margin-bottom:8mm; }}
h1 {{ font-size:26pt; letter-spacing:.06em; color:#16324A; }}
h2 {{ font-size:14pt; letter-spacing:.18em; color:#0077B5; margin-top:2mm; font-weight:600; }}
.periodo {{ font-size:17pt; color:#003A6F; margin:6mm 0 2mm; font-weight:700; }}
.canales {{ font-size:9.5pt; letter-spacing:.1em; color:#878787; margin-bottom:6mm; }}
.metodo {{ font-size:8.4pt; color:#5a6b7a; text-align:justify; line-height:1.45; margin-top:3mm; }}
.sello {{ display:inline-block; margin-top:7mm; padding:1.6mm 6mm; border:1.5px solid #003A6F; border-radius:2mm;
          color:#003A6F; letter-spacing:.22em; font-size:9pt; font-weight:700; }}
.head {{ display:flex; align-items:center; gap:5mm; border-bottom:2.2px solid #003A6F; padding-bottom:2.5mm; margin-bottom:5mm; }}
.minilogo {{ height:9mm; }}
.htxt {{ font-size:8pt; color:#878787; letter-spacing:.05em; }}
.htxt b {{ color:#16324A; }}
.titulo-seccion {{ background:linear-gradient(90deg,#003A6F,#0077B5); color:#fff; font-size:12.5pt; font-weight:700;
  letter-spacing:.08em; padding:3mm 5mm; border-radius:1.5mm; margin-bottom:5mm; }}
.bloque {{ margin-bottom:5mm; }}
.cab {{ display:flex; justify-content:space-between; align-items:baseline; background:#E9F4FA;
  border-left:4px solid #0077B5; padding:2mm 4mm; margin-bottom:0; }}
.dest {{ font-weight:700; font-size:10.5pt; color:#003A6F; letter-spacing:.04em; }}
.cod {{ font-size:8pt; color:#0077B5; letter-spacing:.12em; }}
table {{ width:100%; border-collapse:collapse; font-size:8.2pt; }}
th {{ background:#16324A; color:#fff; font-size:7.4pt; letter-spacing:.08em; text-transform:uppercase;
  padding:2mm 2.4mm; text-align:right; font-weight:600; }}
th:first-child, th:nth-child(2) {{ text-align:left; }}
td {{ padding:1.8mm 2.4mm; border-bottom:.5px solid #d7e2ea; text-align:right; font-variant-numeric:tabular-nums; }}
td:first-child, td:nth-child(2) {{ text-align:left; }}
td.tipo {{ font-size:7.2pt; color:#878787; letter-spacing:.06em; }}
tr.propio td.tipo {{ color:#0077B5; font-weight:700; }}
td.hotel {{ font-weight:600; color:#16324A; }}
td.mejor {{ background:#CCEFFD; font-weight:700; color:#003A6F; }}
td.na, .na {{ color:#B0B6BD; }}
td.vs {{ font-size:7.6pt; color:#5a6b7a; }}
.abajo {{ color:#1A9C4A; font-weight:700; }}
.arriba {{ color:#D43C29; }}
.ref {{ color:#B05C00; font-size:7pt; font-weight:700; }}
.res td {{ font-size:8.4pt; }}
.bench td {{ padding:1.3mm 2mm; font-size:7.7pt; }}
.bench th {{ font-size:6.9pt; padding:1.7mm 2mm; }}
.bench td.hotel {{ font-size:7.7pt; }}
.leyenda {{ font-size:6.9pt; color:#878787; padding:1.6mm 1mm; border-bottom:.5px solid #e3ebf1; }}
.nota {{ font-size:7.6pt; color:#5a6b7a; padding:1.6mm 2mm 0; line-height:1.45; border-left:3px solid #9ED4E9; margin:1.6mm 0 0 1mm; padding-left:3mm; }}
.foot {{ position:absolute; bottom:6mm; left:13mm; right:13mm; display:flex; justify-content:space-between;
  font-size:7pt; color:#878787; border-top:.5px solid #d7e2ea; padding-top:1.6mm; }}
</style></head><body>
{cuerpo}
</body></html>'''

def emitir(version):
    h = html(version)
    base = f'Reporte_Competencia_10-15_Oct_2026_V3_{version.upper()}'
    hf = os.path.join(AQUI, base + '.html')
    pf = os.path.join(AQUI, base + '.pdf')
    with open(hf,'w',encoding='utf-8') as f: f.write(h)
    r = subprocess.run([CHROME,'--headless=new','--no-sandbox','--disable-gpu',
        '--no-pdf-header-footer', f'--print-to-pdf={pf}', 'file://'+hf],
        capture_output=True, text=True, timeout=120)
    ok = os.path.exists(pf) and os.path.getsize(pf) > 10000
    print(base+'.pdf', 'OK' if ok else 'FALLO', os.path.getsize(pf) if ok else r.stderr[-400:])
    return pf

if __name__ == '__main__':
    for v in ('interna','colombia'):
        emitir(v)
