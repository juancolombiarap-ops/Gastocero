# Reporte de Competencia — 10 al 15 de octubre 2026

**El informe es uno solo y su periodo es el 10 al 15 de octubre.** No hay una
segunda corrida ni un informe paralelo del 3 al 8.

La regla es esta: cuando una celda queda **NA** —el hotel cotizado y sin cupo ni
tarifa en esas fechas— se busca una tarifa similar en fechas cercanas y se deja
como **referencia al pie de la tabla**, para que el NA no quede como un vacío. Esa
referencia:

- no reemplaza la celda, que sigue diciendo NA;
- no entra en el cálculo de MEJOR;
- va rotulada como valor referencial, con su fecha y su canal;
- se usa **solo** donde hay NA, no como comparativo general.

Las fechas cercanas que se usaron son el 3 al 8 de octubre, mismo largo de estadía
(5 noches, 2 adultos).

## Celdas NA del 10–15 que necesitan referencia

| Destino | Hotel | Sección | Estado |
|---|---|---|---|
| CTG | Decameron Cartagena | Alojamiento y paquetería | NA en los cuatro operadores |
| SMR | Decameron Galeón | Alojamiento | NA en los cuatro; en paquetería sí tiene Cocha |
| TBP | Royal Decameron Punta Sal | Alojamiento y paquetería | NA en los cuatro |
| PTY | Grand Decameron Panamá | Banco de camas, Cocha y Expedia | sin tarifa; pendiente reconfirmar en Cocha |

## Qué se verificó

El canal directo (decameronchile.cl) sí tiene cupo del 3 al 8 de octubre en los tres
hoteles que estaban bloqueados. Cotizado el 29/08/2026, total de la estadía en USD,
2 adultos, tarifa más económica de cada modalidad:

| Hotel | 3–8 Oct (No Reemb.) | 3–8 Oct (Flex) | 10–15 Oct |
|---|---|---|---|
| Decameron Cartagena | $1,063 | $1,179 | NA |
| Decameron Galeón (Santa Marta) | $1,245 | $1,381 | NA |
| Royal Decameron Punta Sal | $1,567 | NA | NA |

El resto de la nómina propia en el mismo periodo: Isleño $1,491 / $1,655 ·
San Luis $748 / $829 · Marazul $930 / $1,031 · Los Delfines $1,083 / $1,201 ·
Barú $1,681 / $1,866 · Grand Decameron Panamá $875 (solo No Reembolsable).

Decameron Maryland figura NA, pero **no** por el cambio de fechas: sale NA también
en el 10–15 de octubre. El canal directo no lo está publicando; en las OTA sí tenía
tarifa en la corrida anterior, así que hay que cotizarlo igual.

Datos crudos en `dchile_03-08_Oct_2026.json` (formato de caché que consume
`informe.py --dchile-json`) y `dchile_10-15_Oct_2026_control.json` (el control que
respalda los NA del periodo anterior).

## Lo que falta

Las cuatro columnas OTA — V. Falabella, Despegar, Cocha y Expedia — y la tabla de
aéreos siguen pendientes: hay que cotizarlas a mano o desde el equipo donde corre el
flujo habitual. No se pudieron levantar acá.

## Planilla de insumo

`Reporte_Competencia_03-08_Oct_2026_PLANTILLA.xlsx` trae la nómina completa del
informe V.2 (38 hoteles por sección, 7 rutas aéreas), las celdas de precio vacías y
el periodo ya cargado en T2/U2 de la hoja TABLA, que es de donde `informe.py` saca
el rotulado. Está validada contra `mapa.py`: 38 filas de alojamiento, 38 de
paquetería y 7 rutas, todo dentro de las 135 filas que ese parser escanea.

Convención de carga: celda vacía = canal no cotizado (N/D); cero o texto = cotizado
sin disponibilidad ni tarifa (NA).

Para regenerarla con otras fechas:

    py -3 generar_plantilla.py 2026-10-03 2026-10-08 [SALIDA.xlsx]

Y para emitir el informe una vez cargada:

    py -3 informe.py "Reporte_Competencia_03-08_Oct_2026_PLANTILLA.xlsx" --version colombia
    py -3 informe.py "Reporte_Competencia_03-08_Oct_2026_PLANTILLA.xlsx" --version interna \
          --dchile-json dchile_03-08_Oct_2026.json --dchile-fecha "29/08/2026 17:00"

## Estimado del 3–8 para las tablas del 10–15

Cartagena, Santa Marta y Punta Sal salen NA en el informe del 10–15 de octubre.
Para que ese NA no quede como un vacío, el estimado del 3 al 8 se deja como nota al
pie de las seis tablas: las cuatro de alojamiento y las cuatro de paquetería.

Misma base que el resto del informe: 2 adultos, habitación Standard, tarifa más
económica de esa categoría, total de la estadía en USD. Canal directo, verificado
con tres muestras idénticas el 31/08/2026:

| Hotel | Habitación | No Reemb. | Flex | Por noche |
|---|---|---|---|---|
| Decameron Cartagena | Estándar | $979 | $1,085 | $196 |
| Decameron Galeón | Estándar | $1,245 | $1,381 | $249 |
| Royal Decameron Punta Sal | Superior Plus | $1,524 (sin rótulo) | — | $305 |
| Grand Decameron Panamá | Garden View | $875 (sin rótulo) | — | $175 |

**No Reembolsable y Flex son dos tarifas distintas**, no dos precios de lo mismo.
Cada modalidad queda sujeta a sus propias condiciones de cambio y cancelación, y esas
condiciones el canal las describe recién al momento de reservar. La brecha entre las
dos —$106 en Cartagena, $136 en Galeón— es el costo de la flexibilidad, no un
descuento: por eso van en columnas separadas y no se promedian ni se elige una como
«la» tarifa del hotel sin decir cuál es.

Eso también condiciona la comparación contra los operadores: de las celdas de las OTA
no conocemos la condición de la tarifa. Cuando se contrasta el $979 No Reembolsable de
Cartagena contra un $1,136 de Falabella, se están comparando **precios, no productos**.
Punta Sal y Panamá ni siquiera rotulan modalidad en la ficha, así que de esos dos no se
declara ninguna de las dos.

Todo esto va rotulado en las notas como **valor referencial**: es de otro periodo y
de un canal distinto de los cuatro operadores, así que no reemplaza la cotización de
las tablas ni entra en el cálculo de MEJOR.

**La tarifa del canal directo se mueve.** Entre el 29/08 y el 31/08 Cartagena bajó de
$1,063 a $979, y Punta Sal dejó de publicar la Estándar vista al mar Plus ($1,567):
hoy su única categoría es Superior Plus ($1,524). Por eso cada nota lleva su fecha de
cotización y conviene volver a correr `cotizar_directo.py` justo antes de emitir. Las
cifras del 29/08 quedan superadas por estas.

Punta Sal y Panamá son el caso de la regla de categoría: **ninguno publica Standard**
en esas fechas, así que la cifra es de la categoría disponible —Superior Plus y Garden
View— y queda declarada en la nota. En Galeón la Standard sí está disponible.

Aparte, la carga de banco de camas de Panamá figura sin tarifa en Cocha y Expedia en
el 10–15: **queda pendiente reconfirmarla en el motor de Cocha antes de emitir** —
desde este entorno Cocha no responde a ninguna consulta con fechas.

`categorias.py` es lo que resuelve esto: `dchile.cotizar_modalidades()` devuelve la
tarifa más barata pero no dice de qué habitación es, y una cifra sin categoría no es
comparable con el resto de la tabla. Devuelve la categoría elegida, si es la básica
o no, y las demás que ofrece el hotel.

`notas_estimado_03-08_oct.py` trae las ocho notas listas para pegar dentro de
`NOTAS_DESTINO_POR_PERIODO` en `informe.py`. Ojo con un detalle: `leer()` hace
`NOTAS_DESTINO.update(...)`, así que la clave del periodo **reemplaza** a la de
`NOTAS_DESTINO_BASE` en vez de sumarse — por eso las dos entradas de TBP repiten la
nota estructural de la zona. Si no se repite, se pierde del PDF.

En paquetería la nota no lleva cifra, y es a propósito. El canal directo no vende
hotel más aéreo — `informe.py` mismo le pone NA a esa columna — y las cuatro OTA no
se pudieron cotizar. Sumar alojamiento más aéreo por separado tampoco sirve: la
columna de paquetería es el paquete que arma el operador, otro producto, y el número
no sería comparable con el resto de la tabla.

Un matiz de Santa Marta: en paquetería el Galeón **no** está NA en el 10–15, tiene
$3,357 en Cocha. Solo está sin cupo en alojamiento. La nota de paquetería está
redactada para ese caso y no repite que esté sin disponibilidad.

El estimado es de otro periodo y de un canal distinto de los cuatro operadores: va
solo al pie, no entra en las tablas ni en el cálculo de MEJOR, y no se compara
contra las tarifas del 10–15.

Para rehacerlo o extenderlo a otros hoteles:

    py -3 cotizar_directo.py 2026-10-03 2026-10-08 [HOTEL ...]

Datos crudos en `estimado_03-08_Oct_2026_CTG_SMR_TBP.json`.

## Referencias del 3–8 que aportaron los operadores

Estas son las cotizaciones que Juan levantó a mano en cada motor, porque desde este
entorno las cuatro OTA no responden. Van al pie de las tablas del 10–15 como valor
referencial, igual que las del canal directo: **no** reemplazan la celda NA ni entran
en MEJOR.

| Destino | Hotel | Sección | Canal | USD | Observación |
|---|---|---|---|---|---|
| PTY | Grand Decameron Panamá | Alojamiento | V. Falabella | $1,480 | falta categoría |
| PTY | Grand Decameron Panamá | Paquetería | V. Falabella | $2,555 | $2.409.546 CLP |
| CTG | Decameron Cartagena | Alojamiento | V. Falabella | $1,136 | promocional −35% |
| CTG | Decameron Cartagena | Paquetería | V. Falabella | NA | cotizado, sin cupo |
| SMR | Decameron Galeón | Alojamiento | V. Falabella | $1,682 | «Solo queda 1» |
| SMR | Decameron Galeón | Alojamiento | Despegar | $1,660 | «Solo queda 1» |
| SMR | Decameron Galeón | Paquetería | Despegar | $2,651 | vuelo con escalas SCL↔SMR |
| TBP | Royal Decameron Punta Sal | Alojamiento | V. Falabella | NA | cotizado, sin cupo |
| TBP | Royal Decameron Punta Sal | Paquetería | V. Falabella | NA | cotizado, sin cupo |

Del Galeón hay tres precios para las mismas fechas y el mismo producto: Despegar
$1,660, V. Falabella $1,682 y canal directo $1,245. La brecha contra el directo —más
de $400— hay que leerla con cuidado, porque las dos tarjetas de OTA dicen **«Solo
queda 1»**: es precio de última habitación, no la tarifa corriente del hotel.

**Tarifas atadas a un medio de pago.** Despegar publica el Galeón en $1.535.022
«Con Cencosud», o sea $1,628. Ese monto **no** se carga en la tabla: una tarifa que
depende de una tarjeta no compara con el resto de las celdas. Queda solo como
mención, mismo criterio que se aplicó a Punta Sal.

**El paquete del Galeón en Despegar** son $2.499.506 CLP por las dos personas
—el sitio publica $1.249.753 por persona— o sea **$2,651**, con vuelo con escalas
SCL↔SMR e impuestos, tasas y cargos incluidos. Sirve de referencia porque la celda de
Despegar en paquetería de Santa Marta **también está NA** en el 10–15: lo único que
tiene esa fila es el $3,357 de Cocha.

Y da una lectura de paso: entre el paquete ($2,651) y el alojamiento solo ($1,660)
del mismo canal y las mismas fechas quedan unos $991 por las dos personas, que es lo
que Despegar le está poniendo al aéreo. Es una cifra creíble para un SCL↔SMR con
escalas, así que las dos cotizaciones se sostienen entre sí.

Lo que todavía falta de referencias: Santa Marta paquetería en Falabella, y Despegar,
Cocha y Expedia para Cartagena y Punta Sal, más Cocha y Expedia en Santa Marta.
Detalle crudo en `ota_03-08_oct_2026.json`.

## Moneda: todo en dólares

Todas las cifras del informe van en **USD**, sin excepción. Cuando el operador
publica en pesos chilenos se convierte al tipo de cambio del informe, **$943 por
dólar**, y se guarda también el monto original en pesos para poder rehacer la
conversión si el cambio se actualiza.

Conversiones hechas hasta ahora:

| Origen | CLP | USD |
|---|---|---|
| Panamá, paquetería, V. Falabella | $2.409.546 | $2.555 |
| Barú, paquetería | $2.855.740 | $3.028 |
| Galeón, alojamiento 3–8, Despegar | $1.565.022 | $1,660 |
| Galeón, alojamiento 3–8, Despegar «Con Cencosud» | $1.535.022 | $1,628 |
| Galeón, paquetería 3–8, Despegar | $2.499.506 | $2,651 |
| ~~Punta Sal, alojamiento, Despegar~~ | ~~$1.501.980~~ | ~~$1,593~~ |

La última fila queda **descartada**: esa búsqueda salió con fechas de septiembre, así
que Punta Sal sigue en NA. Se deja tachada para que no se vuelva a cargar por error.

## Sobre la planilla del 3–8

`Reporte_Competencia_03-08_Oct_2026_PLANTILLA.xlsx` se armó antes de que quedara
clara la regla de arriba, pensando en una corrida completa del 3 al 8. **No es eso
lo que se necesita.** Sirve igual como insumo para cotizar las referencias, pero el
informe que se emite es el del 10–15; esa planilla no se convierte en un segundo
reporte.

## Cargas dobles: se muestra solo la más barata

Cuando un operador carga el mismo hotel por dos vías —la tarifa que suple Decameron
Chile y la de un banco de camas— el informe mostraba **las dos filas**, rotuladas, con
una nota explicando la diferencia. Desde el 31/08 se muestra **solo la más baja**, que
es la que la representación mantiene en el mercado.

Lo que se pierde con eso: gerencia deja de ver que el mismo hotel está cargado más
caro por otra vía. Por eso la nota al pie de la tabla dice cuánto quedaba la carga que
no se publica.

**Y no se afirma de quién es cada carga.** `marcar_fuentes()` lo deduce comparando
precios: asume que la más barata es la que suple Decameron Chile y la otra un banco de
camas. Es una regla de dedo, no un dato verificado con el operador — si la suposición
falla, el informe estaría rotulando mal el origen. Mientras nadie lo confirme, las
filas van descritas como «segunda carga del hotel», sin nombrar proveedor.

Único caso hoy, Grand Decameron Panamá:

| Sección | Carga más baja (se publica) | Carga más alta (no se publica) |
|---|---|---|
| Alojamiento | $956 | $1,177 |
| Paquetería | $2,273 | $2,756 |

Al sacar la carga de banco de camas de paquetería, el más caro de esa tabla pasa a ser
Dreams Playa Bonita con $2,496.

En `informe.py` esto vive en `marcar_fuentes()` y en `tabla_destino()`: hoy conservan
las dos filas y las rotulan con `ETIQUETA_FUENTE`. Para dejar solo la más barata hay
que descartar la fila `bedbank` cuando existe una `propia` con precio.

## Dos juegos de notas: interna y Colombia

El informe que se manda a Colombia **no puede mostrar decameron.com ni
decameronchile.cl**. `informe.py` ya les quita la columna en `VERSIONES['colombia']`,
pero las notas al pie no las filtra nadie — y todo el estimado del 3 al 8 sale
justamente del canal directo. Tal cual estaba, la cifra se habría ido igual en la
versión Colombia, por la puerta de atrás.

Por eso `notas_estimado_03-08_oct.py` trae dos diccionarios:

- `NOTAS_10_15_OCT_INTERNA` — con la referencia del canal directo, para uso interno.
- `NOTAS_10_15_OCT_COLOMBIA` — sin la cifra y sin mencionar la venta web directa.
  Deja lo que sí es de los operadores: que el hotel está sin cupo en los cuatro, la
  contradicción del Galeón y el pendiente de Cocha en Panamá. Donde antes iba la
  cifra, dice que el hotel sí tiene disponibilidad del 3 al 8 y que esa cotización
  se maneja aparte.

En `leer()`, donde hoy dice `NOTAS_DESTINO.update(NOTAS_DESTINO_POR_PERIODO...)`,
hay que elegir el juego según la versión que se emite; el archivo trae el snippet.
`leer()` hoy recibe solo el set de canales a excluir, así que lo más corto es
pasarle también `args.version` desde `main()`.


## Punto a revisar antes de emitir

En el V.2, Decameron Barú aparece solo en el benchmark y no en la tabla de Cartagena.
En esta planilla Barú quedó con destino CTG, así que saldría también en esa tabla.
Si se quiere mantener el corte anterior, hay que darle a esa fila el mismo código de
destino que traía el Excel original.

También quedan por confirmar los puntajes entre paréntesis de las dos cargas de
Grand Decameron Panamá: la planilla usa (7.5) banco de camas y (7.8) nuestra tarifa,
que son los del V.2, pero los operadores los mueven de una corrida a otra.
