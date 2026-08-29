# -*- coding: utf-8 -*-
"""Cotiza en el canal directo los hoteles que se quieran, para un periodo.

Sirve para armar el estimado que va como nota al pie cuando un hotel propio sale
NA en los operadores. Usa dchile.py, el mismo módulo del flujo del informe.

Uso: py -3 cotizar_directo.py 2026-10-03 2026-10-08 [HOTEL ...]
Sin hoteles, cotiza los tres que salieron NA en el 10-15 de octubre.
"""
import datetime as dt
import json
import sys

import dchile

POR_DEFECTO = ['DECAMERON CARTAGENA', 'DECAMERON GALEON', 'ROYAL DECAMERON PUNTA SAL']
NOCHES = 5


def main():
    ini, fin = sys.argv[1], sys.argv[2]
    hoteles = sys.argv[3:] or POR_DEFECTO
    sello = dt.datetime.now().strftime('%d/%m/%Y %H:%M')
    out = {'cotizado': sello, 'periodo': f'{ini} a {fin}', 'noches': NOCHES, 'pax': 2,
           'fuente': 'decameronchile.cl (canal directo)', 'hoteles': {}}
    for h in hoteles:
        slug = dchile.SLUGS.get(h)
        if not slug:
            print(f'{h}: sin slug en dchile.SLUGS, se omite')
            continue
        r = dchile.cotizar_modalidades(slug, ini, fin)
        # Por noche, que es como se lee un estimado suelto fuera de la tabla.
        r['NR_noche'] = round(r['NR'] / NOCHES) if isinstance(r['NR'], int) else 'NA'
        r['FLEX_noche'] = round(r['FLEX'] / NOCHES) if isinstance(r['FLEX'], int) else 'NA'
        out['hoteles'][h] = r
        print(f'{h}: No Reemb. {r["NR"]} ({r["NR_noche"]}/noche) | Flex {r["FLEX"]}')
    destino = f'estimado_{ini}_a_{fin}.json'
    with open(destino, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f'\nGuardado en {destino} (sello {sello})')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    main()
