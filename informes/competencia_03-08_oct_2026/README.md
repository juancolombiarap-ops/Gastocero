# Reporte de Competencia — 3 al 8 de octubre 2026

Corrida nueva, pedida porque en el periodo 10–15 de octubre los hoteles propios de
Cartagena, Santa Marta (Galeón) y Punta Sal salían NA en los cuatro operadores.

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
pie de las seis tablas: las tres de alojamiento y las tres de paquetería.

Misma base que el resto del informe: 2 adultos, habitación Standard, tarifa más
económica de esa categoría, total de la estadía en USD. Canal directo, cotizado el
29/08/2026 21:56:

| Hotel | Habitación | No Reemb. | Flex | Por noche |
|---|---|---|---|---|
| Decameron Cartagena | Estándar | $1,063 | $1,179 | $213 |
| Decameron Galeón | Estándar | $1,245 | $1,381 | $249 |
| Royal Decameron Punta Sal | Estándar vista al mar Plus | $1,567 (sin rótulo) | — | $313 |

Dos cosas de Punta Sal, que son justamente el caso de la regla: **no ofrece Standard
a secas** en esas fechas, así que la cifra es de la categoría siguiente disponible
—Estándar vista al mar Plus— y queda declarado en la nota; la de más arriba,
Superior Plus, sale $1,615. Y su ficha no rotula modalidad, así que el monto no se
puede presentar como No Reembolsable ni como Flex. En Galeón la categoría siguiente
es Villa, $1,428, pero ahí Standard sí está disponible.

`categorias.py` es lo que resuelve esto: `dchile.cotizar_modalidades()` devuelve la
tarifa más barata pero no dice de qué habitación es, y una cifra sin categoría no es
comparable con el resto de la tabla. Devuelve la categoría elegida, si es la básica
o no, y las demás que ofrece el hotel.

`notas_estimado_03-08_oct.py` trae las seis notas listas para pegar dentro de
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

## Punto a revisar antes de emitir

En el V.2, Decameron Barú aparece solo en el benchmark y no en la tabla de Cartagena.
En esta planilla Barú quedó con destino CTG, así que saldría también en esa tabla.
Si se quiere mantener el corte anterior, hay que darle a esa fila el mismo código de
destino que traía el Excel original.

También quedan por confirmar los puntajes entre paréntesis de las dos cargas de
Grand Decameron Panamá: la planilla usa (7.5) banco de camas y (7.8) nuestra tarifa,
que son los del V.2, pero los operadores los mueven de una corrida a otra.
