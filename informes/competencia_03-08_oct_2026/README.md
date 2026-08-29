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

## Punto a revisar antes de emitir

En el V.2, Decameron Barú aparece solo en el benchmark y no en la tabla de Cartagena.
En esta planilla Barú quedó con destino CTG, así que saldría también en esa tabla.
Si se quiere mantener el corte anterior, hay que darle a esa fila el mismo código de
destino que traía el Excel original.

También quedan por confirmar los puntajes entre paréntesis de las dos cargas de
Grand Decameron Panamá: la planilla usa (7.5) banco de camas y (7.8) nuestra tarifa,
que son los del V.2, pero los operadores los mueven de una corrida a otra.
