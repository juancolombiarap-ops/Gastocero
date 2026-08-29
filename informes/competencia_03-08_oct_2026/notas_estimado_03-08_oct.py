# -*- coding: utf-8 -*-
"""Notas al pie con el estimado del 3-8 de octubre, para el informe del 10-15.

Los hoteles propios de Cartagena, Santa Marta y Punta Sal salen NA en el periodo
10-15 de octubre. Estas notas dejan asentado, debajo de cada tabla —alojamiento y
paquetería—, qué pasa del 3 al 8, para que el NA se lea con una referencia al lado
en vez de un vacío.

Se pega dentro de NOTAS_DESTINO_POR_PERIODO en informe.py, como una clave más.

OJO: leer() hace NOTAS_DESTINO.update(...), o sea que la clave del periodo
REEMPLAZA a la de NOTAS_DESTINO_BASE, no se suma. Por eso las entradas de TBP
—las dos, alojamiento y paquetería— repiten la nota base de la zona: si no se
repite, se pierde del PDF.

ALOJAMIENTO: cifras del canal directo (decameronchile.cl), 2 adultos, 5 noches,
total de la estadía en USD, cotizado el 29/08/2026 21:49. Origen: cotizar_directo.py.

PAQUETERÍA: no hay estimado propio del 3-8. El canal directo no vende paquetes con
aéreo —informe.py mismo le pone NA a esa columna— y las cuatro OTA no se pudieron
cotizar. Sumar hotel + aéreo por separado tampoco sirve: la columna de paquetería
es el paquete que arma el operador, otro producto, y el número no sería comparable.
Así que la nota de paquetería dice qué se sabe y qué falta, sin inventar la cifra.
"""

# Referencia de alojamiento del 3 al 8 de octubre (canal directo, total estadía).
_REF = {
    'CTG': 'US$ 1.063 No Reembolsable y US$ 1.179 Flex (US$ 213 por noche)',
    'SMR': 'US$ 1.245 No Reembolsable y US$ 1.381 Flex (US$ 249 por noche)',
    'TBP': 'US$ 1.567 No Reembolsable, sin modalidad Flex publicada (US$ 313 por noche)',
}
_ZONA_TBP = ('Sin oferta All Inclusive comparable en la zona; el contraste se realiza '
             'entre operadores sobre el mismo producto Decameron.')
_SIN_PAQUETE = ('Para esas fechas no se cotizó paquete: el canal directo no vende '
                'hotel más aéreo y los cuatro operadores no se pudieron consultar. '
                'La referencia de arriba es solo alojamiento y no es comparable con '
                'esta tabla.')

NOTAS_10_15_OCT = {
    ('2026-10-10', '2026-10-15'): {
        ('ALOJAMIENTO', 'CTG'): [
            'DECAMERON CARTAGENA figura NA porque está sin cupo para estas fechas en '
            'los cuatro operadores y también en la venta web directa. Como referencia, '
            f'del 3 al 8 de octubre sí hay tarifa en el canal directo: {_REF["CTG"]} '
            'por la estadía, cotizado el 29/08/2026.',
        ],
        ('PAQUETERÍA', 'CTG'): [
            'DECAMERON CARTAGENA figura sin disponibilidad en los cuatro operadores '
            'para estas fechas. Del 3 al 8 de octubre el hotel sí se vende: el canal '
            f'directo lo cotiza en {_REF["CTG"]} por la estadía, solo alojamiento. '
            + _SIN_PAQUETE,
        ],
        ('ALOJAMIENTO', 'SMR'): [
            'DECAMERON GALEÓN figura NA porque está sin cupo para estas fechas en los '
            'cuatro operadores y también en la venta web directa. Como referencia, del '
            f'3 al 8 de octubre sí hay tarifa en el canal directo: {_REF["SMR"]} por la '
            'estadía, cotizado el 29/08/2026.',
        ],
        ('PAQUETERÍA', 'SMR'): [
            'DECAMERON GALEÓN sí tiene paquete para estas fechas (Cocha), aunque en '
            'alojamiento puro esté sin cupo en los cuatro operadores. Del 3 al 8 de '
            f'octubre el canal directo lo cotiza en {_REF["SMR"]} por la estadía, solo '
            'alojamiento; el paquete de esas fechas queda pendiente de cotizar en los '
            'operadores.',
        ],
        ('ALOJAMIENTO', 'TBP'): [
            # Se repite la nota estructural de la zona: la clave del periodo reemplaza
            # a NOTAS_DESTINO_BASE en lugar de sumarse.
            _ZONA_TBP,
            'ROYAL DECAMERON PUNTA SAL figura NA porque está sin cupo para estas fechas '
            'en los cuatro operadores y también en la venta web directa. Como '
            f'referencia, del 3 al 8 de octubre sí hay tarifa en el canal directo: '
            f'{_REF["TBP"]} por la estadía, cotizado el 29/08/2026.',
        ],
        ('PAQUETERÍA', 'TBP'): [
            _ZONA_TBP,
            'ROYAL DECAMERON PUNTA SAL figura sin disponibilidad en los cuatro '
            'operadores para estas fechas. Del 3 al 8 de octubre el hotel sí se vende: '
            f'el canal directo lo cotiza en {_REF["TBP"]} por la estadía, solo '
            'alojamiento. ' + _SIN_PAQUETE,
        ],
    },
}

# El estimado es del canal directo y de OTRAS fechas: no entra en las tablas ni en
# los cálculos de MEJOR, y no se compara contra las tarifas del 10-15, que son de
# otro periodo. Va solo como nota al pie.
