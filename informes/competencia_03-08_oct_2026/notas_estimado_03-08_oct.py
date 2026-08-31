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

VALOR REFERENCIAL. Todo lo que va en estas notas es una referencia de otro
periodo y de un canal distinto de los cuatro operadores: no reemplaza la
cotización de las tablas ni entra en el cálculo de MEJOR. Cada nota lo dice con
esas palabras, para que gerencia no lea la cifra como si fuera del 10-15.

BASE DE COMPARACIÓN. Igual que el resto del informe: 2 adultos, habitación
Standard, tarifa más económica de esa categoría, total de la estadía en USD.
Cuando el hotel no tiene Standard en esas fechas se toma la categoría siguiente
y se declara en la nota, que es lo que pasa con Punta Sal. Cifras del canal
directo (decameronchile.cl), cotizadas el 31/08/2026 con categorias.py y
verificadas con tres muestras idénticas.

  Cartagena   Estándar                      979 No Reemb. / 1.085 Flex  (196/noche)
  Galeón      Estándar                    1.245 No Reemb. / 1.381 Flex  (249/noche)
              (la otra categoría de la ficha es Villa)
  Punta Sal   Superior Plus               1.524                         (305/noche)
              Es la ÚNICA categoría que publica: no hay Standard. Sin rótulo
              de modalidad, así que el monto no se declara ni No Reembolsable
              ni Flex.
  Panamá      Garden View                   875                         (175/noche)
              Tampoco publica Standard; la otra es Ocean View Plus. Sin
              rótulo de modalidad.

LA TARIFA DEL CANAL DIRECTO SE MUEVE. Entre el 29/08 y el 31/08 cambiaron
Cartagena (1.063 -> 979) y Punta Sal, que además dejó de publicar la Estándar
vista al mar Plus y hoy solo ofrece Superior Plus (1.567 -> 1.524). Por eso cada
nota lleva su fecha de cotización: sin ese sello la cifra no se puede auditar.
Antes de emitir conviene volver a correr cotizar_directo.py y actualizar.

PAQUETERÍA: no hay estimado propio del 3-8. El canal directo no vende paquetes con
aéreo —informe.py mismo le pone NA a esa columna— y las cuatro OTA no se pudieron
cotizar. Sumar hotel + aéreo por separado tampoco sirve: la columna de paquetería
es el paquete que arma el operador, otro producto, y el número no seria comparable.
Así que la nota de paquetería dice qué se sabe y qué falta, sin inventar la cifra.
"""

_ZONA_TBP = ('Sin oferta All Inclusive comparable en la zona; el contraste se realiza '
             'entre operadores sobre el mismo producto Decameron.')
_SIN_OTA = ('Esa referencia es solo del canal directo: para el 3 al 8 los cuatro '
            'operadores no se pudieron cotizar, así que no hay comparativo de '
            'mercado para esas fechas.')
_SIN_PAQUETE = ('Para esas fechas no se cotizó paquete: el canal directo no vende '
                'hotel más aéreo y los cuatro operadores no se pudieron consultar. '
                'La referencia de arriba es solo alojamiento y no es comparable con '
                'esta tabla.')

# Referencia de alojamiento del 3 al 8 de octubre, con la categoría declarada.
_CTG = ('habitación Estándar, US$ 979 No Reembolsable y US$ 1.085 Flex por la '
        'estadía (US$ 196 por noche)')
_SMR = ('habitación Estándar, US$ 1.245 No Reembolsable y US$ 1.381 Flex por la '
        'estadía (US$ 249 por noche)')
_PTY = ('US$ 875 por la estadía (US$ 175 por noche) en Garden View: el hotel no '
        'publica Standard a secas en esas fechas, así que se toma la categoría '
        'siguiente disponible, Garden View, y se declara. Sin rótulo de modalidad')
_TBP = ('US$ 1.524 por la estadía (US$ 305 por noche) en Superior Plus, única '
        'categoría que el hotel publica para esas fechas: no ofrece Standard, así '
        'que la cifra corresponde a una categoría superior y queda declarada. La '
        'ficha no rotula la modalidad, de modo que el monto no se declara como No '
        'Reembolsable ni como Flex')

NOTAS_10_15_OCT = {
    ('2026-10-10', '2026-10-15'): {
        ('ALOJAMIENTO', 'CTG'): [
            'DECAMERON CARTAGENA figura NA porque está sin cupo para estas fechas en '
            'los cuatro operadores y también en la venta web directa. Como VALOR REFERENCIAL —otro periodo, otro canal—, '
            f'del 3 al 8 de octubre sí hay tarifa en el canal directo: {_CTG}. '
            'Cotizado el 31/08/2026. ' + _SIN_OTA,
        ],
        ('PAQUETERÍA', 'CTG'): [
            'DECAMERON CARTAGENA figura sin disponibilidad en los cuatro operadores '
            'para estas fechas. Del 3 al 8 de octubre el hotel sí se vende; a modo de VALOR REFERENCIAL, el canal '
            f'directo lo cotiza en {_CTG}, solo alojamiento. ' + _SIN_PAQUETE,
        ],
        ('ALOJAMIENTO', 'SMR'): [
            'DECAMERON GALEÓN figura NA porque está sin cupo para estas fechas en los '
            'cuatro operadores y también en la venta web directa. Como VALOR REFERENCIAL —otro periodo, otro canal—, del '
            f'3 al 8 de octubre sí hay tarifa en el canal directo: {_SMR}. Cotizado el '
            '31/08/2026. ' + _SIN_OTA,
        ],
        ('PAQUETERÍA', 'SMR'): [
            'DECAMERON GALEÓN sí tiene paquete para estas fechas (Cocha), aunque en '
            'alojamiento puro esté sin cupo en los cuatro operadores. Del 3 al 8 de '
            f'octubre el canal directo lo cotiza en {_SMR}, solo alojamiento; el '
            'paquete de esas fechas queda pendiente de cotizar en los operadores.',
        ],
        ('ALOJAMIENTO', 'PTY'): [
            'GRAND DECAMERON PANAMÁ: la carga de banco de camas figura sin tarifa en '
            'Cocha y Expedia para estas fechas; queda pendiente reconfirmarla en el '
            'motor de Cocha antes de emitir. Como VALOR REFERENCIAL —otro periodo, '
            f'otro canal—, del 3 al 8 de octubre el canal directo lo cotiza en {_PTY}. '
            'Cotizado el 31/08/2026. ' + _SIN_OTA,
        ],
        ('PAQUETERÍA', 'PTY'): [
            'GRAND DECAMERON PANAMÁ: del 3 al 8 de octubre el canal directo cotiza el '
            f'hotel en {_PTY}, solo alojamiento y como VALOR REFERENCIAL. ' + _SIN_PAQUETE,
        ],
        ('ALOJAMIENTO', 'TBP'): [
            # Se repite la nota estructural de la zona: la clave del periodo reemplaza
            # a NOTAS_DESTINO_BASE en lugar de sumarse.
            _ZONA_TBP,
            'ROYAL DECAMERON PUNTA SAL figura NA porque está sin cupo para estas fechas '
            'en los cuatro operadores y también en la venta web directa. Como VALOR '
            f'REFERENCIAL —otro periodo, otro canal—, del 3 al 8 de octubre el canal '
            f'directo sí lo vende: {_TBP}. '
            'Cotizado el 31/08/2026. ' + _SIN_OTA,
        ],
        ('PAQUETERÍA', 'TBP'): [
            _ZONA_TBP,
            'ROYAL DECAMERON PUNTA SAL figura sin disponibilidad en los cuatro '
            'operadores para estas fechas. Del 3 al 8 de octubre el hotel sí se vende; a modo de VALOR REFERENCIAL, '
            f'el canal directo lo cotiza en {_TBP}, solo alojamiento. ' + _SIN_PAQUETE,
        ],
    },
}

# El estimado es del canal directo y de OTRAS fechas: no entra en las tablas ni en
# los cálculos de MEJOR, y no se compara contra las tarifas del 10-15, que son de
# otro periodo. Va solo como nota al pie.
