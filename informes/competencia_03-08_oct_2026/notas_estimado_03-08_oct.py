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

BASE DE COMPARACIÓN. Igual que el resto del informe: 2 adultos, habitación
Standard, tarifa más económica de esa categoría, total de la estadía en USD.
Cuando el hotel no tiene Standard en esas fechas se toma la categoría siguiente
y se declara en la nota, que es lo que pasa con Punta Sal. Cifras del canal
directo (decameronchile.cl), cotizadas el 29/08/2026 21:56 con categorias.py.

  Cartagena   Estándar                    1.063 No Reemb. / 1.179 Flex  (213/noche)
  Galeón      Estándar                    1.245 No Reemb. / 1.381 Flex  (249/noche)
              (la siguiente, Villa, 1.428 / 1.585)
  Punta Sal   Estándar vista al mar Plus  1.567                         (313/noche)
              NO hay Standard a secas; la siguiente es Superior Plus, 1.615.
              La ficha no rotula modalidad, así que el monto no se puede
              declarar como No Reembolsable ni como Flex.

PAQUETERÍA: no hay estimado propio del 3-8. El canal directo no vende paquetes con
aéreo —informe.py mismo le pone NA a esa columna— y las cuatro OTA no se pudieron
cotizar. Sumar hotel + aéreo por separado tampoco sirve: la columna de paquetería
es el paquete que arma el operador, otro producto, y el número no seria comparable.
Así que la nota de paquetería dice qué se sabe y qué falta, sin inventar la cifra.
"""

_ZONA_TBP = ('Sin oferta All Inclusive comparable en la zona; el contraste se realiza '
             'entre operadores sobre el mismo producto Decameron.')
_SIN_PAQUETE = ('Para esas fechas no se cotizó paquete: el canal directo no vende '
                'hotel más aéreo y los cuatro operadores no se pudieron consultar. '
                'La referencia de arriba es solo alojamiento y no es comparable con '
                'esta tabla.')

# Referencia de alojamiento del 3 al 8 de octubre, con la categoría declarada.
_CTG = ('habitación Estándar, US$ 1.063 No Reembolsable y US$ 1.179 Flex por la '
        'estadía (US$ 213 por noche)')
_SMR = ('habitación Estándar, US$ 1.245 No Reembolsable y US$ 1.381 Flex por la '
        'estadía (US$ 249 por noche)')
_TBP = ('US$ 1.567 por la estadía (US$ 313 por noche) en Estándar vista al mar Plus: '
        'el hotel no ofrece Standard a secas en esas fechas, así que se toma la '
        'categoría siguiente disponible, y la de más arriba, Superior Plus, sale '
        'US$ 1.615. La ficha no rotula la modalidad, de modo que el monto no se '
        'declara como No Reembolsable ni como Flex')

NOTAS_10_15_OCT = {
    ('2026-10-10', '2026-10-15'): {
        ('ALOJAMIENTO', 'CTG'): [
            'DECAMERON CARTAGENA figura NA porque está sin cupo para estas fechas en '
            'los cuatro operadores y también en la venta web directa. Como referencia, '
            f'del 3 al 8 de octubre sí hay tarifa en el canal directo: {_CTG}. '
            'Cotizado el 29/08/2026.',
        ],
        ('PAQUETERÍA', 'CTG'): [
            'DECAMERON CARTAGENA figura sin disponibilidad en los cuatro operadores '
            'para estas fechas. Del 3 al 8 de octubre el hotel sí se vende: el canal '
            f'directo lo cotiza en {_CTG}, solo alojamiento. ' + _SIN_PAQUETE,
        ],
        ('ALOJAMIENTO', 'SMR'): [
            'DECAMERON GALEÓN figura NA porque está sin cupo para estas fechas en los '
            'cuatro operadores y también en la venta web directa. Como referencia, del '
            f'3 al 8 de octubre sí hay tarifa en el canal directo: {_SMR}; la categoría '
            'siguiente, Villa, sale US$ 1.428. Cotizado el 29/08/2026.',
        ],
        ('PAQUETERÍA', 'SMR'): [
            'DECAMERON GALEÓN sí tiene paquete para estas fechas (Cocha), aunque en '
            'alojamiento puro esté sin cupo en los cuatro operadores. Del 3 al 8 de '
            f'octubre el canal directo lo cotiza en {_SMR}, solo alojamiento; el '
            'paquete de esas fechas queda pendiente de cotizar en los operadores.',
        ],
        ('ALOJAMIENTO', 'TBP'): [
            # Se repite la nota estructural de la zona: la clave del periodo reemplaza
            # a NOTAS_DESTINO_BASE en lugar de sumarse.
            _ZONA_TBP,
            'ROYAL DECAMERON PUNTA SAL figura NA porque está sin cupo para estas fechas '
            'en los cuatro operadores y también en la venta web directa. Como '
            f'referencia, del 3 al 8 de octubre el canal directo sí lo vende: {_TBP}. '
            'Cotizado el 29/08/2026.',
        ],
        ('PAQUETERÍA', 'TBP'): [
            _ZONA_TBP,
            'ROYAL DECAMERON PUNTA SAL figura sin disponibilidad en los cuatro '
            'operadores para estas fechas. Del 3 al 8 de octubre el hotel sí se vende: '
            f'el canal directo lo cotiza en {_TBP}, solo alojamiento. ' + _SIN_PAQUETE,
        ],
    },
}

# El estimado es del canal directo y de OTRAS fechas: no entra en las tablas ni en
# los cálculos de MEJOR, y no se compara contra las tarifas del 10-15, que son de
# otro periodo. Va solo como nota al pie.
