# -*- coding: utf-8 -*-
"""Notas al pie con el estimado del 3-8 de octubre, para el informe del 10-15.

Los tres hoteles propios de Cartagena, Santa Marta y Punta Sal salen NA en el
periodo 10-15 de octubre. Estas notas dejan asentado, debajo de cada tabla, que
del 3 al 8 sí hay tarifa y cuánto, para que gerencia lea el NA con una referencia
al lado en vez de un vacío.

Se pega dentro de NOTAS_DESTINO_POR_PERIODO en informe.py, como una clave más.

OJO: leer() hace NOTAS_DESTINO.update(...), o sea que la clave del periodo
REEMPLAZA a la de NOTAS_DESTINO_BASE, no se suma. Por eso la entrada de TBP
repite la nota base de la zona: si no se repite, se pierde.

Cifras del canal directo (decameronchile.cl), 2 adultos, 5 noches, total de la
estadía en USD, cotizado el 29/08/2026 21:49. Origen: cotizar_directo.py.
"""

NOTAS_10_15_OCT = {
    ('2026-10-10', '2026-10-15'): {
        ('ALOJAMIENTO', 'CTG'): [
            'DECAMERON CARTAGENA figura NA porque está sin cupo para estas fechas en '
            'los cuatro operadores y también en la venta web directa. Como referencia, '
            'del 3 al 8 de octubre sí hay tarifa en el canal directo: US$ 1.063 No '
            'Reembolsable y US$ 1.179 Flex por la estadía (US$ 213 por noche), '
            'cotizado el 29/08/2026.',
        ],
        ('ALOJAMIENTO', 'SMR'): [
            'DECAMERON GALEÓN figura NA porque está sin cupo para estas fechas en los '
            'cuatro operadores y también en la venta web directa. Como referencia, del '
            '3 al 8 de octubre sí hay tarifa en el canal directo: US$ 1.245 No '
            'Reembolsable y US$ 1.381 Flex por la estadía (US$ 249 por noche), '
            'cotizado el 29/08/2026.',
        ],
        ('ALOJAMIENTO', 'TBP'): [
            # Se repite la nota estructural de la zona: la clave del periodo reemplaza
            # a NOTAS_DESTINO_BASE en lugar de sumarse.
            'Sin oferta All Inclusive comparable en la zona; el contraste se realiza '
            'entre operadores sobre el mismo producto Decameron.',
            'ROYAL DECAMERON PUNTA SAL figura NA porque está sin cupo para estas fechas '
            'en los cuatro operadores y también en la venta web directa. Como '
            'referencia, del 3 al 8 de octubre sí hay tarifa en el canal directo: '
            'US$ 1.567 No Reembolsable por la estadía (US$ 313 por noche); la modalidad '
            'Flex no está publicada. Cotizado el 29/08/2026.',
        ],
    },
}

# El estimado es del canal directo y de OTRAS fechas: no entra en las tablas ni en
# los cálculos de MEJOR, y no se compara contra las tarifas OTA del 10-15, que son
# de otro periodo. Va solo como nota al pie.
