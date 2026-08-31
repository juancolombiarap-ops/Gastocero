# -*- coding: utf-8 -*-
"""Cotiza el canal directo declarando la CATEGORÍA de habitación de cada tarifa.

El reporte compara habitación Standard, 2 adultos. Cuando el hotel no tiene
Standard disponible en esas fechas se toma la categoría siguiente y hay que
declararla: una cifra sin categoría no es comparable con el resto de la tabla.
dchile.cotizar_modalidades() devuelve la tarifa más barata pero no dice de qué
habitación es; esto lo resuelve.

El sitio renderiza cada habitación como <h3>Habitación <!-- -->NOMBRE</h3> y más
abajo sus tarifas rotuladas No Reembolsable / Flex. Se recorre el HTML en orden:
cada precio pertenece al último nombre de habitación visto antes de él.
"""
import re

import dchile

HAB_RE = re.compile(r'Habitaci[oó]n\s*<!-- -->([^<]{1,80})</h3>')
# Palabras que suben de categoría: si acompañan a 'Estándar', ya no es la básica.
# 'Estándar vista al mar Plus' no lo es; 'Estándar Twin/king' sí —eso es tipo de
# cama, no categoría— y 'Estándar / Junior Suite' también, porque el sitio ofrece
# las dos en la misma ficha y la tarifa que se toma es la de la Estándar.
UPGRADE_RE = re.compile(r'vista|mar|plus|superior|deluxe|premium|familiar|villa|'
                        r'bungalow|ocean|garden|suite', re.I)


def es_basica(nombre):
    """True si la habitación es la Standard a secas (admite tipo de cama)."""
    n = nombre.split('/')[0].strip()
    if not re.match(r'^est[áa]ndar\b', n, re.I):
        return False
    resto = re.sub(r'^est[áa]ndar\b', '', n, flags=re.I)
    return not UPGRADE_RE.search(resto)


def _tokens(html):
    """(posición, tipo, valor) de habitaciones, modalidades y precios, en orden."""
    out = []
    for m in HAB_RE.finditer(html):
        out.append((m.start(), 'hab', m.group(1).strip()))
    for m in dchile.TOKEN_RE.finditer(html):
        if m.group(1):
            out.append((m.start(), 'mod', m.group(1)))
        else:
            out.append((m.start(), 'precio', float(m.group(2).replace(',', ''))))
    out.sort(key=lambda t: t[0])
    return out


def habitaciones(slug, fecha_in, fecha_out):
    """[{'habitacion', 'NR', 'FLEX', 'modalidad_rotulada'}] en orden del sitio.

    No todas las fichas rotulan la modalidad: Punta Sal, por ejemplo, publica un
    precio por habitación y nada de No Reembolsable / Flex. En ese caso el monto
    va a NR —es lo que hace dchile.cotizar()— pero queda marcado como no
    rotulado, porque afirmar que es No Reembolsable seria inventarlo.
    """
    html = dchile._html(slug, fecha_in, fecha_out)
    if not html:
        return []
    tokens = _tokens(html)
    rotula = any(t[1] == 'mod' for t in tokens)
    filas, mod = [], None
    for _pos, tipo, valor in tokens:
        if tipo == 'hab':
            filas.append({'habitacion': valor, 'NR': 'NA', 'FLEX': 'NA',
                          'modalidad_rotulada': rotula})
        elif tipo == 'mod':
            mod = valor
        elif tipo == 'precio' and filas:
            clave = 'FLEX' if mod == 'Flex' else 'NR'
            # La primera tarifa de cada modalidad es la más barata de esa habitación.
            if filas[-1][clave] == 'NA':
                filas[-1][clave] = round(valor)
    return [f for f in filas if f['NR'] != 'NA' or f['FLEX'] != 'NA']


def cotizar(slug, fecha_in, fecha_out):
    """La habitación más económica disponible, con su categoría declarada."""
    filas = habitaciones(slug, fecha_in, fecha_out)
    con_precio = [f for f in filas if isinstance(f['NR'], int)]
    if not con_precio:
        return {'habitacion': None, 'NR': 'NA', 'FLEX': 'NA', 'es_standard': None,
                'categorias_ofrecidas': [f['habitacion'] for f in filas]}
    elegida = min(con_precio, key=lambda f: f['NR'])
    return {
        'habitacion': elegida['habitacion'],
        'NR': elegida['NR'],
        'FLEX': elegida['FLEX'],
        'modalidad_rotulada': elegida['modalidad_rotulada'],
        'es_standard': es_basica(elegida['habitacion']),
        'categorias_ofrecidas': [f['habitacion'] for f in filas],
    }
