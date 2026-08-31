// Reporte de Competencia 10-15 Oct 2026 en PowerPoint.
// Tablas nativas editables, paleta e identidad del informe original.
//   node generar_ppt_reporte.js colombia   |   node generar_ppt_reporte.js interna

const fs = require('fs');
const pptxgen = require('pptxgenjs');

const version = (process.argv[2] || 'colombia').toLowerCase();
const D = JSON.parse(fs.readFileSync(`datos_word_${version}.json`, 'utf8'));
const LOGO = 'image/png;base64,' + fs.readFileSync('marca/logo_decameron.png').toString('base64');
const GRAD = 'image/jpeg;base64,' + fs.readFileSync('marca/portada_gradiente.jpg').toString('base64');

// paleta del informe
const TINTA='16324A', MARCA='003A6F', ACENTO='0077B5', CELESTE='CCEFFD', SUAVE='EFF7FC';
const GRIS='878787', VERDE='15793C', ROJO='BF382A', AMBAR='8A5A00', AMBAR_BG='FBF2DF';
const TEXTO='3E5265', LINEA='D6DFE7', NA='B0B6BD';

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';                       // 13.3 x 7.5
pres.author = 'Hoteles Decameron Chile';
pres.title  = `Reporte de Competencia 10-15 Octubre 2026`;
const W = 13.3, H = 7.5, M = 0.55;

const sello = version === 'interna' ? 'VERSIÓN INTERNA' : 'VERSIÓN COLOMBIA';

// -------------------------------------------------------------- helpers
function cabecera(s, titulo, sub) {
  s.addImage({ data: LOGO, x: M, y: 0.30, w: 1.55, h: 0.60 });
  s.addText([{ text:'REPORTE DE COMPETENCIA', options:{ bold:true, color:TINTA } },
             { text:'  ·  periodo 10 – 15 Octubre 2026  ·  V.3', options:{ color:GRIS } }],
    { x:2.25, y:0.34, w:W-2.25-M, h:0.25, fontSize:9, fontFace:'Calibri', isTextBox:true, margin:0 });
  s.addText(titulo, { x:2.25, y:0.58, w:W-2.25-M-2.4, h:0.42, fontSize:22, bold:true,
    color:MARCA, fontFace:'Calibri', isTextBox:true, margin:0 });
  if (sub) s.addText(sub, { x:2.25, y:0.99, w:W-2.25-M-2.4, h:0.22, fontSize:9.5,
    color:GRIS, fontFace:'Calibri', isTextBox:true, margin:0 });
  s.addShape(pres.ShapeType.line, { x:M, y:1.26, w:W-2*M, h:0, line:{ color:MARCA, width:1.6 } });
}

function pie(s, izq, num) {
  s.addShape(pres.ShapeType.line, { x:M, y:H-0.52, w:W-2*M, h:0, line:{ color:LINEA, width:0.75 } });
  s.addText(izq, { x:M, y:H-0.47, w:8.5, h:0.24, fontSize:8, color:GRIS, fontFace:'Calibri',
    isTextBox:true, margin:0 });
  s.addText(String(num), { x:W-M-1.2, y:H-0.47, w:1.2, h:0.24, fontSize:8, color:GRIS,
    align:'right', fontFace:'Calibri', isTextBox:true, margin:0 });
}

const celda = (t,o={}) => ({ text:t, options:{ fontSize:o.fs||9.5, bold:o.b, color:o.c||TEXTO,
  align:o.al||'right', fill:o.fill?{color:o.fill}:undefined, valign:'middle', fontFace:'Calibri' } });

function tablaDestino(s, t, y) {
  const cols = [1.05, 3.05, 1.35, 1.25, 1.15, 1.25, 1.55];
  const head = ['TIPO','HOTEL','V. FALABELLA','DESPEGAR','COCHA','EXPEDIA','MEJOR'];
  const rows = [ head.map((h,i)=>celda(h,{fs:8, b:true, c:'FFFFFF', fill:TINTA,
    al: i<2 ? 'left':'right'})) ];
  for (const f of t.filas) {
    const bg = f.propio ? SUAVE : 'FFFFFF';
    const r = [ celda(f.tipo, {fs:7.5, al:'left', c:f.propio?ACENTO:GRIS, b:f.propio, fill:bg}),
                celda(f.hotel, {fs:9, al:'left', b:true, c:TINTA, fill:bg}) ];
    f.vals.forEach(v => r.push(celda(v, {c:(v==='NA'||v==='N/D')?NA:TEXTO, fill:bg})));
    const m = f.mejor;
    r.push(celda(m, { b:true, fill:CELESTE,
      c: m.includes('▼')?VERDE : m.includes('▲')?ROJO : MARCA }));
    rows.push(r);
  }
  s.addTable(rows, { x:M, y, w:W-2*M, colW:cols, border:{type:'solid',color:LINEA,pt:0.5},
    autoPage:false, rowH:0.245 });
  return y + 0.245*rows.length + 0.06;
}

function notas(s, t, y) {
  s.addText(D.leyenda, { x:M, y, w:W-2*M, h:0.2, fontSize:7, color:GRIS, fontFace:'Calibri',
    isTextBox:true, margin:0 });
  y += 0.22;
  for (const n of t.notas) {
    const alto = Math.max(0.3, Math.ceil(n.length/168)*0.17 + 0.13);
    s.addShape(pres.ShapeType.rect, { x:M, y, w:0.045, h:alto, fill:{color:'9ED4E9'}, line:{width:0} });
    s.addText(n, { x:M+0.14, y, w:W-2*M-0.14, h:alto, fontSize:7.8, color:'5A6B7A',
      fontFace:'Calibri', isTextBox:true, margin:0, valign:'top' });
    y += alto + 0.06;
  }
  return y;
}

// -------------------------------------------------------------- 1. portada
{
  const s = pres.addSlide();
  s.background = { data: GRAD };
  s.addShape(pres.ShapeType.roundRect, { x:1.5, y:0.55, w:W-3, h:H-1.1,
    fill:{color:'FFFFFF'}, line:{width:0}, rectRadius:0.06,
    shadow:{ type:'outer', color:'000000', blur:14, offset:4, angle:90, opacity:0.28 } });
  s.addImage({ data: LOGO, x:(W-3.5)/2, y:0.95, w:3.5, h:1.36 });
  s.addText('REPORTE DE COMPETENCIA', { x:2, y:2.42, w:W-4, h:0.55, fontSize:32, bold:true,
    color:TINTA, align:'center', fontFace:'Calibri', isTextBox:true });
  s.addText('HOTELES DECAMERON CHILE', { x:2, y:2.95, w:W-4, h:0.32, fontSize:15, bold:true,
    color:ACENTO, align:'center', charSpacing:2, fontFace:'Calibri', isTextBox:true });
  s.addText('10 – 15 Octubre 2026', { x:2, y:3.38, w:W-4, h:0.42, fontSize:23, bold:true,
    color:MARCA, align:'center', fontFace:'Calibri', isTextBox:true });
  s.addText('CANALES:  V. FALABELLA   |   DESPEGAR   |   COCHA   |   EXPEDIA',
    { x:2, y:3.82, w:W-4, h:0.26, fontSize:10, color:GRIS, align:'center', charSpacing:1,
      fontFace:'Calibri', isTextBox:true });

  s.addShape(pres.ShapeType.rect, { x:2.05, y:4.32, w:0.05, h:1.32, fill:{color:'E08A1E'}, line:{width:0} });
  s.addShape(pres.ShapeType.rect, { x:2.10, y:4.32, w:W-4.15, h:1.32, fill:{color:AMBAR_BG},
    line:{color:'E8CE96', width:0.75} });
  s.addText([
    { text:'EL PERIODO DE ESTE REPORTE ES EL 10 AL 15 DE OCTUBRE DE 2026. ', options:{bold:true, color:AMBAR} },
    { text:'Todas las tablas, los cálculos de MEJOR y las comparaciones corresponden únicamente a esas fechas. Donde una celda queda en NA —hotel cotizado, sin cupo ni tarifa— la nota al pie puede incluir una cotización del ', options:{color:'5C4310'} },
    { text:'3 al 8 de octubre', options:{bold:true, color:AMBAR} },
    { text:': esa cifra es ', options:{color:'5C4310'} },
    { text:'SOLO REFERENCIAL', options:{bold:true, color:AMBAR} },
    { text:', pertenece a otro periodo, no reemplaza la celda, no entra en ningún cálculo del informe y no debe compararse con las tarifas de las tablas.', options:{color:'5C4310'} },
  ], { x:2.28, y:4.42, w:W-4.6, h:1.12, fontSize:10, fontFace:'Calibri', isTextBox:true,
       margin:0, valign:'middle' });

  s.addText(sello, { x:(W-3.2)/2, y:5.85, w:3.2, h:0.38, fontSize:11, bold:true, color:MARCA,
    align:'center', charSpacing:2, fontFace:'Calibri', isTextBox:true,
    line:{color:MARCA, width:1}, rectRadius:0.04 });
  s.addText('Cotización 27/08/2026  ·  re-cotización y verificación 31/08/2026  ·  conversión CLP→USD $943',
    { x:2, y:6.42, w:W-4, h:0.26, fontSize:9, color:GRIS, align:'center', fontFace:'Calibri', isTextBox:true });
  s.addNotes(`Reporte de competencia del 10 al 15 de octubre de 2026. ${sello}. Cuatro operadores: V. Falabella, Despegar, Cocha y Expedia. Precios en USD, total de la estadía para dos adultos, habitación Standard. Las cifras del 3 al 8 de octubre que aparecen en notas son solo referenciales.`);
}

// -------------------------------------------------------------- 2. metodología
{
  const s = pres.addSlide();
  cabecera(s, 'Cómo leer este reporte', 'Base de comparación, convenciones y correcciones de la V.3');
  const cards = [
    ['BASE DE COMPARACIÓN','2 adultos · 5 noches · habitación Standard (si no hay, la categoría siguiente, declarada) · tarifa más económica de esa categoría · régimen All Inclusive donde aplica · total de la estadía en USD · conversión CLP→USD $943.'],
    ['CONVENCIONES','MEJOR = tarifa más baja de los cuatro operadores.  ▼ más económico de la tabla  ·  ▲ más caro.  NA = se cotizó y no había disponibilidad ni tarifa.  N/D = ese canal no se cotizó para ese hotel.'],
    ['QUÉ CAMBIÓ EN LA V.3','Panamá y Galeón recotizados en Cocha por hotel y fecha ($963 y $1,461). Barú corregido en alojamiento ($2,142) y paquetería ($3,028). Cargas dobles publicadas por su tarifa más baja, sin rotular origen.'],
    ['LO QUE HAY QUE SABER','En Cocha ningún hotel Decameron aparece en la búsqueda por destino: todos hubo que encontrarlos por nombre. Las celdas son correctas, pero el cliente que busca por destino no llega a estos hoteles.'],
  ];
  let y = 1.55;
  cards.forEach(([t, d], i) => {
    const x = i % 2 === 0 ? M : W/2 + 0.1;
    if (i % 2 === 0 && i > 0) y += 2.35;
    const dest = i === 3;
    s.addShape(pres.ShapeType.roundRect, { x, y, w:(W-2*M-0.2)/2, h:2.15,
      fill:{color: dest ? AMBAR_BG : 'F7FBFD'},
      line:{ color: dest ? 'E8CE96' : LINEA, width:0.75 }, rectRadius:0.03 });
    s.addText(t, { x:x+0.22, y:y+0.16, w:(W-2*M-0.2)/2-0.44, h:0.3, fontSize:11, bold:true,
      color: dest ? AMBAR : MARCA, fontFace:'Calibri', isTextBox:true, margin:0 });
    s.addText(d, { x:x+0.22, y:y+0.52, w:(W-2*M-0.2)/2-0.44, h:1.5, fontSize:10,
      color: dest ? '5C4310' : TEXTO, fontFace:'Calibri', isTextBox:true, margin:0, valign:'top' });
  });
  pie(s, 'Metodología', 2);
  s.addNotes('La base de comparación es la misma para todos los operadores: dos adultos, cinco noches, habitación Standard y tarifa más económica de esa categoría. NA significa que se cotizó y no había cupo; N/D que ese canal no se consultó para ese hotel.');
}

// -------------------------------------------------------------- secciones
let n = 3;
function seccionPortadilla(titulo, sub, notaVoz) {
  const s = pres.addSlide();
  s.background = { color: TINTA };
  s.addImage({ data: LOGO, x:M, y:0.4, w:1.7, h:0.66 });
  s.addText(titulo, { x:M, y:H/2-0.9, w:W-2*M, h:0.9, fontSize:40, bold:true, color:'FFFFFF',
    fontFace:'Calibri', isTextBox:true });
  s.addText(sub, { x:M, y:H/2+0.05, w:W-2*M, h:0.4, fontSize:14, color:'9ED4E9',
    fontFace:'Calibri', isTextBox:true });
  s.addNotes(notaVoz);
  n++;
}

function slidesDeSeccion(tablas, etiqueta) {
  for (const t of tablas) {
    const s = pres.addSlide();
    cabecera(s, `${etiqueta} · ${t.destino}`, `${t.cod} · 10 – 15 Octubre 2026 · 2 adultos · USD`);
    let y = tablaDestino(s, t, 1.45);
    notas(s, t, y);
    pie(s, `${etiqueta} · ${t.destino}`, n);
    const propios = t.filas.filter(f=>f.propio).map(f=>`${f.hotel} ${f.mejor}`).join('; ');
    s.addNotes(`${etiqueta} en ${t.destino}. Hoteles propios: ${propios || 'sin fila propia en esta tabla'}.`);
    n++;
  }
}

function slideBench(rows, titulo, sub, ref) {
  const s = pres.addSlide();
  cabecera(s, titulo, sub);
  const cols = [0.95, 2.55, 0.6, 1.15, 1.05, 0.95, 1.0, 1.35, 1.2];
  const head = ['CATEGORÍA','HOTEL','DEST','V. FALABELLA','DESPEGAR','COCHA','EXPEDIA','MEJOR','VS ISLEÑO'];
  const filas = [ head.map((h,i)=>celda(h,{fs:7, b:true, c:'FFFFFF', fill:TINTA, al:i<2?'left':'right'})) ];
  for (const r of rows) {
    const bg = r.propio ? SUAVE : 'FFFFFF';
    const fila = [ celda(r.cat,{fs:7, al:'left', c:r.propio?ACENTO:GRIS, b:r.propio, fill:bg}),
                   celda(r.hotel,{fs:8, al:'left', b:true, c:TINTA, fill:bg}),
                   celda(r.dest,{fs:7, c:GRIS, fill:bg}) ];
    r.vals.forEach(v => fila.push(celda(v,{fs:8, c:(v==='NA'||v==='N/D')?NA:TEXTO, fill:bg})));
    fila.push(celda(r.mejor,{fs:8, b:true, fill:CELESTE,
      c: r.mejor.includes('▼')?VERDE : r.mejor.includes('★')?AMBAR : MARCA }));
    fila.push(celda(r.vs,{fs:7.5, c:'5A6B7A', fill:bg}));
    filas.push(fila);
  }
  s.addTable(filas, { x:M, y:1.45, w:W-2*M, colW:cols, border:{type:'solid',color:LINEA,pt:0.5},
    autoPage:false, rowH:0.222 });
  s.addText(`★ REF = referencia del benchmark (Isleño ${ref}, mejor tarifa OTA)  |  ▼ competidor más económico  |  Última columna, base precio del competidor: Isleño +X% = el Isleño está X% más caro que ese hotel; Isleño −X% = está X% más barato. MEJOR considera solo canales OTA.`,
    { x:M, y:1.45+0.222*filas.length+0.07, w:W-2*M, h:0.3, fontSize:7, color:GRIS,
      fontFace:'Calibri', isTextBox:true, margin:0 });
  pie(s, 'Benchmark internacional', n);
  s.addNotes(`Benchmark del Isleño contra la competencia internacional en Punta Cana, Cancún y Curazao. La última columna dice cuánto más caro o más barato está el Isleño respecto de cada competidor.`);
  n++;
}

seccionPortadilla('Alojamiento', 'Seis destinos · 10 al 15 de octubre de 2026 · 2 adultos, USD',
  'Empieza la sección de alojamiento: solo hotel, sin aéreo, para los seis destinos del informe.');
slidesDeSeccion(D.aloj, 'Alojamiento');
slideBench(D.bench_aloj, 'Alojamiento — Isleño vs competencia internacional',
  'Referencia: Decameron Isleño $1,467, mejor tarifa OTA', '$1,467');

seccionPortadilla('Paquetería', 'Hotel + aéreo · 10 al 15 de octubre de 2026 · 2 adultos, USD',
  'Sección de paquetería: el paquete que arma cada operador, hotel más aéreo. Es otro producto, no la suma de las partes.');
slidesDeSeccion(D.paq, 'Paquetería');
slideBench(D.bench_paq, 'Paquetería — Isleño vs competencia internacional',
  'Referencia: Decameron Isleño $2,074, mejor tarifa OTA', '$2,074');

// -------------------------------------------------------------- aéreos
{
  const s = pres.addSlide();
  cabecera(s, 'Tarifas aéreas desde Santiago', 'SCL · 10 – 15 Octubre 2026 · por persona, ida y vuelta, USD');
  const cols=[2.1,1.6,1.6,1.6,1.6,1.65,1.65];
  const head=['RUTA','LATAM','AVIANCA','COPA','SKY','JETSMART','ARAJET'];
  const filas=[ head.map((h,i)=>celda(h,{fs:8,b:true,c:'FFFFFF',fill:TINTA,al:i===0?'left':'right'})) ];
  for (const r of D.aereos) {
    const fila=[ celda(r.ruta,{fs:10,al:'left',b:true,c:TINTA}) ];
    r.vals.forEach((v,i)=>{
      const raw=r.raw[i];
      let c=TEXTO,b=false;
      if (v==='NA') c=NA; else if (raw===r.min){c=VERDE;b=true;} else if (raw===r.max) c=ROJO;
      fila.push(celda(v,{fs:10,c,b}));
    });
    filas.push(fila);
  }
  s.addTable(filas,{x:M,y:1.5,w:W-2*M,colW:cols,border:{type:'solid',color:LINEA,pt:0.5},
    autoPage:false,rowH:0.34});
  s.addText('Verde = más barato por ruta   |   Rojo = más caro   |   NA = aerolínea sin vuelo en la ruta',
    {x:M,y:1.5+0.34*filas.length+0.1,w:W-2*M,h:0.24,fontSize:8,color:GRIS,fontFace:'Calibri',
     isTextBox:true,margin:0});
  pie(s,'Tarifas aéreas',n); n++;
  s.addNotes('Tarifas aéreas por persona, ida y vuelta. Ojo: son tarifas base. Ninguna aerolínea incluye maleta de bodega en la tarifa que alimenta los comparadores.');
}

function slideResumen(titulo, sub, cab, rows, nota) {
  const s = pres.addSlide();
  cabecera(s, titulo, sub);
  const k = cab.length;
  const primera = 3.3, resto = (W-2*M-primera)/(k-1);
  const cols = [primera, ...Array(k-1).fill(resto)];
  const filas=[ cab.map((h,i)=>celda(h.toUpperCase(),{fs:8,b:true,c:'FFFFFF',fill:TINTA,
    al:i===0?'left':'right'})) ];
  rows.forEach(r => filas.push(r.map((v,i)=>celda(String(v),
    {fs:10, al:i===0?'left':'right', b:i===0, c:i===0?TINTA:TEXTO}))));
  s.addTable(filas,{x:M,y:1.5,w:W-2*M,colW:cols,border:{type:'solid',color:LINEA,pt:0.5},
    autoPage:false,rowH:0.31});
  if (nota) s.addText(nota,{x:M,y:1.5+0.31*filas.length+0.1,w:W-2*M,h:0.3,fontSize:8,
    color:GRIS,fontFace:'Calibri',isTextBox:true,margin:0});
  pie(s,'Resúmenes',n); n++;
  s.addNotes(titulo);
}

slideResumen('Mejor operador por hotel', 'Alojamiento · dónde está más barato cada hotel propio',
  ['Hotel','Mejor op.','Precio','2do mejor','Precio','Dif'], D.mejor_op,
  'Panamá corregido a $963 (Cocha, recotizado por hotel y fecha). El Galeón queda con Cocha como único canal con tarifa.');
slideResumen('Benchmark Isleño vs competencia internacional', 'Mejor tarifa OTA del Isleño: $1,467',
  ['Competidor','Destino','Mejor OTA','vs Isleño','Dif'], D.bench_res,
  'DIF con base en el precio del competidor: Isleño +X% = el Isleño está X% más caro que ese hotel.');
slideResumen('Mejor aerolínea por ruta', 'Por persona, ida y vuelta, USD',
  ['Ruta','Mejor','Precio','2da opc.','Precio','Dif'], D.mejor_aer);

// -------------------------------------------------------------- cierre
{
  const s = pres.addSlide();
  s.background = { color: TINTA };
  s.addImage({ data: LOGO, x:M, y:0.4, w:1.7, h:0.66 });
  s.addText('Antes de emitir', { x:M, y:1.5, w:W-2*M, h:0.6, fontSize:30, bold:true,
    color:'FFFFFF', fontFace:'Calibri', isTextBox:true });
  const items = [
    'Cocha: ningún hotel Decameron aparece en la búsqueda por destino. Todos hubo que encontrarlos por nombre, incluidos los que sí tienen cupo y tarifa.',
    'Panamá: el $956 que la tabla de verificación atribuye al canal directo no tiene respaldo. Recotizar.',
    'Cartagena: reconfirmar categoría y régimen de Dubai y La Gran Vía; son hoteles urbanos de 3–4 estrellas.',
    'Barú: definir con qué destino queda. Hoy aparece solo en el benchmark, no en la tabla de Cartagena.',
    'Vigencia: las tarifas se cotizaron el 27/08 y se mueven día a día. Barú se movió $214 en cuatro días.',
  ];
  let y = 2.35;
  items.forEach((t,i) => {
    s.addShape(pres.ShapeType.ellipse, { x:M, y:y+0.02, w:0.28, h:0.28, fill:{color:'E08A1E'}, line:{width:0} });
    s.addText(String(i+1), { x:M, y:y+0.02, w:0.28, h:0.28, fontSize:10, bold:true, color:'FFFFFF',
      align:'center', valign:'middle', fontFace:'Calibri', isTextBox:true, margin:0 });
    s.addText(t, { x:M+0.45, y, w:W-2*M-0.45, h:0.62, fontSize:11.5, color:'D5E3EE',
      fontFace:'Calibri', isTextBox:true, margin:0, valign:'top' });
    y += 0.72;
  });
  s.addText('Comparativo entre V. Falabella, Despegar, Cocha y Expedia  ·  Datos del informe V.3  ·  Verificación 31/08/2026',
    { x:M, y:H-0.75, w:W-2*M, h:0.3, fontSize:8.5, color:'7E97AC', fontFace:'Calibri', isTextBox:true });
  s.addNotes('Cinco puntos a cerrar antes de emitir. El más importante es el primero: en Cocha ningún hotel Decameron aparece en la búsqueda por destino.');
}

const out = `Reporte_Competencia_10-15_Oct_2026_V3_${version.toUpperCase()}.pptx`;
pres.writeFile({ fileName: out }).then(() =>
  console.log(out, (fs.statSync(out).size/1024).toFixed(0)+' KB'));
