// Genera el Reporte de Competencia 10-15 Oct 2026 en .docx, con tablas nativas
// editables (no imagenes). Lee datos_word_<version>.json, que exporta emitir_pdf.py.
//
//   node generar_word_reporte.js colombia
//   node generar_word_reporte.js interna

const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType,
  AlignmentType, HeadingLevel, BorderStyle, ShadingType, ImageRun, PageBreak,
  Header, Footer, PageNumber, VerticalAlign,
} = require('docx');

const version = (process.argv[2] || 'colombia').toLowerCase();
const D = JSON.parse(fs.readFileSync(`datos_word_${version}.json`, 'utf8'));
const LOGO = fs.readFileSync('marca/logo_decameron.png');

// paleta de marca, tomada del documento original
const TINTA = '16324A', MARCA = '003A6F', ACENTO = '0077B5', CELESTE = 'CCEFFD';
const GRIS = '878787', VERDE = '15793C', ROJO = 'BF382A', AMBAR = '8A5A00';
const AMBAR_BG = 'FBF2DF', SUAVE = 'EFF7FC';

const ANCHO = 9360;                       // area util A4 con margenes de 1080 dxa
const sinBordes = { top:{style:BorderStyle.NONE}, bottom:{style:BorderStyle.NONE},
                    left:{style:BorderStyle.NONE}, right:{style:BorderStyle.NONE} };

const txt = (text, o={}) => new TextRun({ text, font:'Calibri', size:o.size||18,
  bold:o.bold, italics:o.italics, color:o.color||'3E5265', allCaps:o.caps });

const p = (runs, o={}) => new Paragraph({
  children: Array.isArray(runs) ? runs : [runs],
  alignment: o.align, spacing:{ before:o.before||0, after:o.after===undefined?100:o.after },
  border: o.border, shading: o.shading, indent: o.indent,
});

function celda(children, o={}) {
  return new TableCell({
    children: Array.isArray(children) ? children : [children],
    width: { size:o.w, type:WidthType.DXA },
    shading: o.bg ? { type:ShadingType.CLEAR, fill:o.bg, color:'auto' } : undefined,
    margins: { top:50, bottom:50, left:70, right:70 },
    verticalAlign: VerticalAlign.CENTER,
    columnSpan: o.span,
    borders: { top:{style:BorderStyle.SINGLE,size:1,color:'D6DFE7'},
               bottom:{style:BorderStyle.SINGLE,size:1,color:'D6DFE7'},
               left:{style:BorderStyle.SINGLE,size:1,color:'D6DFE7'},
               right:{style:BorderStyle.SINGLE,size:1,color:'D6DFE7'} },
  });
}

const th = (t, w, align=AlignmentType.RIGHT) =>
  celda(p(txt(t,{bold:true,color:'FFFFFF',size:14}),{align,after:0}), {w, bg:TINTA});

// ---------------------------------------------------------------- tabla destino
function tablaDestino(t, cols) {
  const filas = [ new TableRow({ tableHeader:true, children:[
      th('Tipo',cols[0],AlignmentType.LEFT), th('Hotel',cols[1],AlignmentType.LEFT),
      th('V. Falabella',cols[2]), th('Despegar',cols[3]),
      th('Cocha',cols[4]), th('Expedia',cols[5]), th('Mejor',cols[6]) ]}) ];

  for (const f of t.filas) {
    const bg = f.propio ? SUAVE : undefined;
    const cs = [
      celda(p(txt(f.tipo,{size:13,color:f.propio?ACENTO:GRIS,bold:f.propio}),{after:0}), {w:cols[0],bg}),
      celda(p(txt(f.hotel,{size:16,bold:true,color:TINTA}),{after:0}), {w:cols[1],bg}),
    ];
    f.vals.forEach((v,i) => {
      const na = v==='NA' || v==='N/D';
      cs.push(celda(p(txt(v,{size:16,color:na?'B0B6BD':'3E5265'}),{align:AlignmentType.RIGHT,after:0}),
                    {w:cols[2+i],bg}));
    });
    const m = f.mejor;
    const color = m.includes('▼') ? VERDE : m.includes('▲') ? ROJO : MARCA;
    cs.push(celda(p(txt(m,{size:16,bold:true,color}),{align:AlignmentType.RIGHT,after:0}),
                  {w:cols[6],bg:CELESTE}));
    filas.push(new TableRow({children:cs}));
  }
  return new Table({ columnWidths:cols, width:{size:ANCHO,type:WidthType.DXA}, rows:filas });
}

function bloqueDestino(t, cols) {
  const out = [
    new Table({ columnWidths:[ANCHO*0.75, ANCHO*0.25], width:{size:ANCHO,type:WidthType.DXA},
      rows:[ new TableRow({ children:[
        new TableCell({ width:{size:ANCHO*0.75,type:WidthType.DXA},
          shading:{type:ShadingType.CLEAR,fill:'E9F4FA',color:'auto'}, margins:{top:60,bottom:60,left:120},
          borders:{...sinBordes, left:{style:BorderStyle.SINGLE,size:18,color:ACENTO}},
          children:[p(txt(t.destino,{bold:true,size:21,color:MARCA}),{after:0})] }),
        new TableCell({ width:{size:ANCHO*0.25,type:WidthType.DXA},
          shading:{type:ShadingType.CLEAR,fill:'E9F4FA',color:'auto'}, margins:{top:60,bottom:60,right:120},
          borders:sinBordes,
          children:[p(txt(t.cod,{size:15,color:ACENTO}),{align:AlignmentType.RIGHT,after:0})] }),
      ]})]}),
    tablaDestino(t, cols),
    p(txt(D.leyenda,{size:13,color:GRIS}),{after:60}),
  ];
  for (const n of t.notas) {
    out.push(p(txt(n,{size:15,color:'5A6B7A'}), {
      after:80, indent:{left:180},
      border:{ left:{style:BorderStyle.SINGLE,size:12,color:'9ED4E9',space:8} } }));
  }
  out.push(p(txt(''),{after:120}));
  return out;
}

// ---------------------------------------------------------------- benchmark
function tablaBench(rows, titulo, ref) {
  const c = [820,2180,560,1000,900,800,860,1180,1060];
  const filas = [ new TableRow({ tableHeader:true, children:[
    th('Categoría',c[0],AlignmentType.LEFT), th('Hotel',c[1],AlignmentType.LEFT), th('Dest',c[2]),
    th('V. Falabella',c[3]), th('Despegar',c[4]), th('Cocha',c[5]), th('Expedia',c[6]),
    th('Mejor',c[7]), th('vs Isleño',c[8]) ]}) ];
  for (const r of rows) {
    const bg = r.propio ? SUAVE : undefined;
    const cs = [
      celda(p(txt(r.cat,{size:13,color:r.propio?ACENTO:GRIS,bold:r.propio}),{after:0}),{w:c[0],bg}),
      celda(p(txt(r.hotel,{size:15,bold:true,color:TINTA}),{after:0}),{w:c[1],bg}),
      celda(p(txt(r.dest,{size:13,color:GRIS}),{align:AlignmentType.RIGHT,after:0}),{w:c[2],bg}),
    ];
    r.vals.forEach((v,i)=>{
      const na = v==='NA'||v==='N/D';
      cs.push(celda(p(txt(v,{size:15,color:na?'B0B6BD':'3E5265'}),{align:AlignmentType.RIGHT,after:0}),{w:c[3+i],bg}));
    });
    const color = r.mejor.includes('▼') ? VERDE : r.mejor.includes('★') ? AMBAR : MARCA;
    cs.push(celda(p(txt(r.mejor,{size:15,bold:true,color}),{align:AlignmentType.RIGHT,after:0}),{w:c[7],bg:CELESTE}));
    cs.push(celda(p(txt(r.vs,{size:14,color:'5A6B7A'}),{align:AlignmentType.RIGHT,after:0}),{w:c[8],bg}));
    filas.push(new TableRow({children:cs}));
  }
  return [
    p(txt(titulo,{bold:true,size:21,color:MARCA}),{before:120,after:80}),
    new Table({ columnWidths:c, width:{size:ANCHO,type:WidthType.DXA}, rows:filas }),
    p(txt(`★ REF = referencia del benchmark (Isleño ${ref}, mejor tarifa OTA)  |  ▼ Competidor más económico  |  Última columna, base precio del competidor: Isleño +X% = el Isleño está X% más caro que ese hotel; Isleño −X% = está X% más barato. MEJOR considera solo canales OTA.`,
        {size:13,color:GRIS}),{after:120}),
  ];
}

// ---------------------------------------------------------------- aereos
function tablaAereos() {
  const c=[1660,1280,1280,1280,1280,1290,1290];
  const nombres=['Latam','Avianca','Copa','Sky','JetSmart','Arajet'];
  const filas=[ new TableRow({tableHeader:true, children:[
    th('Ruta',c[0],AlignmentType.LEFT), ...nombres.map((n,i)=>th(n,c[1+i])) ]}) ];
  for (const r of D.aereos) {
    const cs=[ celda(p(txt(r.ruta,{size:16,bold:true,color:TINTA}),{after:0}),{w:c[0]}) ];
    r.vals.forEach((v,i)=>{
      const raw = r.raw[i];
      let color='3E5265', bold=false;
      if (v==='NA') color='B0B6BD';
      else if (raw===r.min) { color=VERDE; bold=true; }
      else if (raw===r.max) color=ROJO;
      cs.push(celda(p(txt(v,{size:16,color,bold}),{align:AlignmentType.RIGHT,after:0}),{w:c[1+i]}));
    });
    filas.push(new TableRow({children:cs}));
  }
  return [
    p(txt('TARIFAS AÉREAS DESDE SANTIAGO',{bold:true,size:21,color:MARCA}),{before:120,after:20}),
    p(txt('SCL · 10 – 15 Octubre 2026 · por persona, ida y vuelta, USD',{size:15,color:GRIS}),{after:80}),
    new Table({columnWidths:c,width:{size:ANCHO,type:WidthType.DXA},rows:filas}),
    p(txt('Verde = más barato por ruta  |  Rojo = más caro  |  NA = aerolínea sin vuelo en la ruta',
      {size:13,color:GRIS}),{after:140}),
  ];
}

function tablaResumen(titulo, cab, rows, nota) {
  const n=cab.length, ancho=Math.floor(ANCHO/n);
  const cols=Array(n).fill(ancho); cols[0]=ANCHO-ancho*(n-1);
  const filas=[ new TableRow({tableHeader:true, children:
    cab.map((t,i)=>th(t,cols[i], i===0?AlignmentType.LEFT:AlignmentType.RIGHT)) }) ];
  for (const r of rows) {
    filas.push(new TableRow({ children: r.map((v,i)=>celda(
      p(txt(String(v),{size:16,bold:i===0,color:i===0?TINTA:'3E5265'}),
        {align:i===0?AlignmentType.LEFT:AlignmentType.RIGHT,after:0}),{w:cols[i]})) }));
  }
  const out=[ p(txt(titulo,{bold:true,size:20,color:MARCA}),{before:120,after:80}),
              new Table({columnWidths:cols,width:{size:ANCHO,type:WidthType.DXA},rows:filas}) ];
  if (nota) out.push(p(txt(nota,{size:13,color:GRIS}),{after:120}));
  else out.push(p(txt(''),{after:120}));
  return out;
}

// ---------------------------------------------------------------- portada
const sello = version==='interna' ? 'VERSIÓN INTERNA' : 'VERSIÓN COLOMBIA';
const portada = [
  p(new ImageRun({type:'png', data:LOGO, transformation:{width:340,height:131}}),
    {align:AlignmentType.CENTER, after:260}),
  p(txt('REPORTE DE COMPETENCIA',{bold:true,size:44,color:TINTA}),{align:AlignmentType.CENTER,after:60}),
  p(txt('HOTELES DECAMERON CHILE',{bold:true,size:24,color:ACENTO}),{align:AlignmentType.CENTER,after:200}),
  p(txt('10 – 15 Octubre 2026',{bold:true,size:30,color:MARCA}),{align:AlignmentType.CENTER,after:60}),
  p(txt('CANALES: V. FALABELLA  |  DESPEGAR  |  COCHA  |  EXPEDIA',{size:16,color:GRIS}),
    {align:AlignmentType.CENTER,after:240}),
  p(txt('Análisis comparativo: Alojamiento, Paquetería y Aéreos. Precios en USD, total de la estadía para 2 adultos, habitación Standard en todos los operadores (si un hotel no tiene Standard disponible se toma la categoría siguiente y se indica en la tabla), tarifa más económica de esa categoría, régimen All Inclusive donde aplica. Datos actualizados al 27/08/2026; Cartagena, Punta Sal y Panamá re-cotizados el 28/08/2026. En la re-cotización, Expedia bloqueó la consulta automática: su columna de alojamiento se obtuvo vía Hoteles.com (mismo grupo e inventario Expedia, precios en USD) y su paquetería quedó sin cotizar (N/D). Conversión CLP→USD al tipo de cambio $943.',
    {size:17,color:'4A5C6E'}),{align:AlignmentType.JUSTIFIED,after:140}),
  p([txt('V.3 — verificación y correcciones del 31/08/2026: ',{bold:true,size:17,color:TINTA}),
     txt('Panamá y Galeón recotizados en Cocha por hotel y fecha ($963 y $1,461: ambos figuraban NA o desactualizados porque el hotel no aparece en la búsqueda de destino de ese operador); Barú corregido en alojamiento ($2,142) y paquetería ($3,028); cargas dobles publicadas por su tarifa más baja, sin rotular origen; celdas NA acompañadas de valor referencial del 3–8 de octubre.'+D.metodo_extra+' Las tarifas se mueven día a día: las cifras son la foto de su fecha de cotización.',
       {size:17,color:'4A5C6E'})],{align:AlignmentType.JUSTIFIED,after:200}),
  p([txt('EL PERIODO DE ESTE REPORTE ES EL 10 AL 15 DE OCTUBRE DE 2026. ',{bold:true,size:17,color:AMBAR}),
     txt('Todas las tablas, los cálculos de MEJOR y las comparaciones corresponden únicamente a esas fechas. Donde una celda queda en NA —hotel cotizado, sin cupo ni tarifa— la nota al pie puede incluir una cotización del ',{size:17,color:'5C4310'}),
     txt('3 al 8 de octubre',{bold:true,size:17,color:AMBAR}),
     txt(': esa cifra es ',{size:17,color:'5C4310'}),
     txt('SOLO REFERENCIAL',{bold:true,size:17,color:AMBAR}),
     txt(', pertenece a otro periodo, no reemplaza la celda, no entra en ningún cálculo del informe y no debe compararse con las tarifas de las tablas. Va identificada en cada caso con la etiqueta VALOR REFERENCIAL.',{size:17,color:'5C4310'})],
    {align:AlignmentType.JUSTIFIED, after:200,
     shading:{type:ShadingType.CLEAR,fill:AMBAR_BG,color:'auto'},
     border:{ left:{style:BorderStyle.SINGLE,size:18,color:'E08A1E',space:10},
              top:{style:BorderStyle.SINGLE,size:6,color:'E8CE96',space:8},
              bottom:{style:BorderStyle.SINGLE,size:6,color:'E8CE96',space:8},
              right:{style:BorderStyle.SINGLE,size:6,color:'E8CE96',space:8} }}),
  p(txt(sello,{bold:true,size:20,color:MARCA}),{align:AlignmentType.CENTER,before:200}),
  p(new PageBreak()),
];

// ---------------------------------------------------------------- cuerpo
const COLS = [1080,2560,1120,1060,980,1060,1500];
const cuerpo = [];
cuerpo.push(p(txt('ALOJAMIENTO',{bold:true,size:28,color:MARCA}),{after:20}));
cuerpo.push(p(txt('10 – 15 Octubre 2026 · 2 adultos · Precios en USD',{size:15,color:GRIS}),{after:160}));
D.aloj.forEach(t => cuerpo.push(...bloqueDestino(t,COLS)));
cuerpo.push(...tablaBench(D.bench_aloj,'ALOJAMIENTO — ISLEÑO VS COMPETENCIA INTERNACIONAL','$1,467'));
cuerpo.push(p(new PageBreak()));

cuerpo.push(p(txt('PAQUETERÍA',{bold:true,size:28,color:MARCA}),{after:20}));
cuerpo.push(p(txt('Hotel + Aéreo · 10 – 15 Octubre 2026 · 2 adultos · Precios en USD',{size:15,color:GRIS}),{after:160}));
D.paq.forEach(t => cuerpo.push(...bloqueDestino(t,COLS)));
cuerpo.push(...tablaBench(D.bench_paq,'PAQUETERÍA — ISLEÑO VS COMPETENCIA INTERNACIONAL','$2,074'));
cuerpo.push(p([txt('DECAMERON BARÚ, paquetería: ',{bold:true,size:15,color:TINTA}),
  txt('celda de V. Falabella corregida el 31/08/2026 de $2,559 a $3,028 (recotización confirmada); con eso el mejor de esa fila pasa a Cocha ($2,605). En alojamiento se corrigió de $1,928 a $2,142, con el periodo confirmado por el calendario del operador. Esa fila mezcla dos fechas de cotización —Despegar del 27/08 y V. Falabella del 31/08—, y esa es la razón de que no coincidan.',
    {size:15,color:'5A6B7A'})],{after:140,indent:{left:180},
    border:{left:{style:BorderStyle.SINGLE,size:12,color:'9ED4E9',space:8}}}));
cuerpo.push(p(new PageBreak()));

cuerpo.push(...tablaAereos());
cuerpo.push(...tablaResumen('MEJOR OPERADOR POR HOTEL — ALOJAMIENTO',
  ['Hotel','Mejor op.','Precio','2do mejor','Precio','Dif'], D.mejor_op,
  'Panamá corregido a $963 (Cocha, recotizado por hotel y fecha). El Galeón queda con Cocha como único canal con tarifa.'));
cuerpo.push(p(new PageBreak()));
cuerpo.push(...tablaResumen('BENCHMARK ISLEÑO (MEJOR TARIFA OTA $1,467) VS COMPETENCIA INTERNACIONAL',
  ['Competidor','Destino','Mejor OTA','vs Isleño','Dif'], D.bench_res,
  'DIF con base en el precio del competidor: Isleño +X% = el Isleño está X% más caro que ese hotel.'));
cuerpo.push(...tablaResumen('MEJOR AEROLÍNEA POR RUTA',
  ['Ruta','Mejor','Precio','2da opc.','Precio','Dif'], D.mejor_aer));

// ---------------------------------------------------------------- documento
const doc = new Document({
  creator:'Hoteles Decameron Chile', title:`Reporte de Competencia 10-15 Octubre 2026 — ${sello}`,
  description:'Comparativo de alojamiento, paquetería y aéreos entre V. Falabella, Despegar, Cocha y Expedia.',
  styles:{ default:{ document:{ run:{ font:'Calibri', size:18, color:'3E5265' } } } },
  sections:[{
    properties:{ page:{ margin:{ top:900, right:1080, bottom:900, left:1080 } } },
    headers:{ default:new Header({ children:[
      p([txt('REPORTE DE COMPETENCIA',{bold:true,size:14,color:TINTA}),
         txt('  ·  Hoteles Decameron Chile  ·  ',{size:14,color:GRIS}),
         txt('periodo 10 – 15 Octubre 2026',{bold:true,size:14,color:TINTA}),
         txt(`  ·  V.3  ·  ${sello.toLowerCase()}  ·  las cifras del 3–8 en las notas son solo referenciales`,{size:14,color:GRIS})],
        {after:40, border:{bottom:{style:BorderStyle.SINGLE,size:12,color:MARCA,space:4}}}) ]}) },
    footers:{ default:new Footer({ children:[
      p([txt('Comparativo entre V. Falabella, Despegar, Cocha y Expedia  ·  ',{size:13,color:GRIS}),
         new TextRun({children:['Página ',PageNumber.CURRENT,' de ',PageNumber.TOTAL_PAGES],
           font:'Calibri', size:13, color:GRIS})],
        {align:AlignmentType.RIGHT, border:{top:{style:BorderStyle.SINGLE,size:4,color:'D6DFE7',space:4}}}) ]}) },
    children:[...portada, ...cuerpo],
  }],
});

Packer.toBuffer(doc).then(b => {
  const out = `Reporte_Competencia_10-15_Oct_2026_V3_${version.toUpperCase()}.docx`;
  fs.writeFileSync(out, b);
  console.log(out, (b.length/1024).toFixed(0)+' KB');
});
