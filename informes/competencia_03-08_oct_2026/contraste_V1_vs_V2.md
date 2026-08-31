# Contraste V.1 vs V.2 del informe 10–15 octubre 2026

Revisión de las tablas de Cartagena, Panamá y Santa Marta entre las dos versiones,
con lo que hay que verificar antes de emitir.

## Panamá — hay un error de número en el V.1

Alojamiento, fila GRAND DECAMERON PANAMÁ «nuestra tarifa»:

| Versión | V. Falabella | Despegar | Cocha | Expedia | MEJOR |
|---|---|---|---|---|---|
| V.1 (6.6) | $1,026 | $1,026 | $1,113 | $1,213 | **$969** |
| V.2 (7.8) | $1,008 | $1,008 | $956 | $1,213 | $956 |

**El $969 del V.1 no sale de ninguna celda de su fila**: el mínimo de esa fila es
$1,026. En el V.2 la misma fila cierra en $956, que sí es el mínimo. El V.1 publicó
un MEJOR que no corresponde.

Además los puntajes se movieron —(7.2)/(6.6) en el V.1 pasaron a (7.5)/(7.8) en el
V.2— y con eso el rótulo «nuestra tarifa» cambió de la 6.6 a la 7.8. Como el rótulo
se asigna por precio y no por puntaje, hay que confirmar que las dos filas siguen
siendo las mismas dos cargas (operador y banco de camas) y no se cruzaron.

Pendiente: la carga de banco de camas figura sin tarifa en Cocha en las dos versiones
(N/A en V.1, NA en V.2). Si en Cocha sí aparece, esa celda hay que cargarla.

## Santa Marta — inconsistencia interna, no entre versiones

Las dos versiones traen exactamente lo mismo:

| Sección | Galeón | Porto Horizonte |
|---|---|---|
| Alojamiento | NA en los cuatro operadores | $1,758 / $1,758 / NA / $1,756 → $1,756 |
| Paquetería | NA / NA / **$3,357** / NA → $3,357 | $2,267 / $3,163 / $2,459 / $2,610 → $2,267 |

**El Galeón aparece sin cupo en alojamiento pero con paquete en Cocha a $3,357.** Si
Cocha vende el paquete es porque el hotel tiene habitaciones, así que el NA de
alojamiento en Cocha no cuadra con su propia paquetería. Hay que rehacer esa celda.

## Cartagena — saltos que no se explican solos

Alojamiento:

| Hotel | V.1 | V.2 |
|---|---|---|
| Decameron Cartagena | fila malformada: `N/A N/A N/A ------`, MEJOR vacío | NA en los cuatro → — |
| Dorado Plaza Bocagrande | NA / NA / $988 / NA → $988 ▼ | $1,132 / $1,132 / $967 / $1,162 → $967 ▲ |
| Hotel Dubai Cartagena | $1,156 / $1,156 / NA / $1,582 → $1,156 | $587 / $587 / $588 / $628 → $587 |
| Hotel La Gran Vía | sin disponibilidad | $580 / $580 / NA / NA → $580 ▼ |
| Cartagena Plaza | sin disponibilidad | sin disponibilidad (Expedia exige mínimo 7 noches) |

Dos cosas para verificar:

1. **Dubai pasó de $1,156 a $587 de un día para otro**, menos de la mitad. Es un
   salto demasiado grande para dejarlo pasar sin confirmar: lo más probable es que
   la re-cotización haya tomado otra categoría o un régimen distinto (solo
   alojamiento en vez de con desayuno / AI).
2. **La Gran Vía pasó de «sin disponibilidad» a ser el más barato de la tabla**
   ($580) y de paso invirtió el orden: el Dorado Plaza, que en el V.1 era el más
   económico, en el V.2 queda marcado como el más caro.

La fila malformada del Decameron Cartagena en el V.1 (tres N/A y un `------`) quedó
bien resuelta en el V.2, que muestra NA en los cuatro operadores.

Paquetería: sin cambios de fondo entre versiones; el V.2 suma La Gran Vía y baja
Dubai, en línea con lo de arriba.

## Punta Sal

NA en los cuatro operadores en alojamiento y en paquetería, en las dos versiones.
Consistente; no hay nada que corregir ahí.
