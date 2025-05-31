"""
Este fichero contiene la función 'normalizaHoras', que detecta  y normaliza expresiones horarias
en un texte, convirtiéndolas al formato HH:MM.

Arnau Piñero Masegosa
"""

import re

def normalizaHoras(ficText, ficNorm):
    """
    Lee el fichero ficText, y normaliza las expresiones horarias como por ejemplo:

    - 8h30m -> 08:30
    - 7h -> 07:00
    - 08:05 -> 08:05
    - 5 menos cuarto -> 04:45
    - 6 y media -> 06:30
    - 8 en punto -> 08:00
    """

    patrones = [
    # hh:mm exacto
    (re.compile(r'\b(\d{1,2}):([0-5]\d)\b'), lambda h, m: f'{int(h):02d}:{int(m):02d}'),

    # HHhMMm como 7h o 7h30m
    (re.compile(r'\b(\d{1,2})h(?:(\d{1,2})m)?\b'), lambda h, m=None: f'{int(h):02d}:{int(m):02d}' if m is not None and int(m) < 60 else (f'{int(h):02d}:00' if m is None else f'{h}h{m}m')),

    # habladas: "x en punto"
    (re.compile(r'\b(\d{1,2})\s+en punto\b'), lambda h: f'{int(h):02d}:00' if 1 <= int(h) <= 12 else f'{h} en punto'),

    # habladas: "x y media"
    (re.compile(r'\b(\d{1,2})\s+y media\b'), lambda h: f'{int(h):02d}:30' if 1 <= int(h) <= 12 else f'{h} y media'),

    # habladas: "x y cuarto"
    (re.compile(r'\b(\d{1,2})\s+y cuarto\b'), lambda h: f'{int(h):02d}:15' if 1 <= int(h) <= 12 else f'{h} y cuarto'),

    # habladas: "x menos cuarto"
    (re.compile(r'\b(\d{1,2})\s+menos cuarto\b'), lambda h: f'{(int(h)-1)%12:02d}:45' if 1 <= int(h) <= 12 else f'{h} menos cuarto'),

    # con referencias de momento del día
    (re.compile(r'\b(1[0-2]|[1-9])\s+de la mañana\b'), lambda h: f'{int(h):02d}:00'),
    (re.compile(r'\b(1[0-2]|[1-9])\s+del mediodía\b'), lambda h: f'{(12 if int(h) == 12 else int(h)):02d}:00'),
    (re.compile(r'\b(1[0-2]|[1-9])\s+de la tarde\b'), lambda h: f'{(int(h)+12)%24:02d}:00' if int(h) < 12 else f'{h} de la tarde'),
    (re.compile(r'\b(1[0-2]|[1-9])\s+de la noche\b'), lambda h: f'{(int(h)+12)%24:02d}:00' if int(h) != 12 else '00:00'),
    (re.compile(r'\b(1[0-2]|[1-9])\s+de la madrugada\b'), lambda h: f'{int(h)%12:02d}:00'),
    ]

    with open(ficText, 'rt', encoding='utf-8') as fin, open(ficNorm, 'wt', encoding='utf-8') as fout:
        for linea in fin:
            original = linea
            for patron, formato in patrones:
                def reemplazo(match):
                    try:
                        return formato(*match.groups())
                    except:
                        return match.group(0)
                linea = patron.sub(reemplazo, linea)
            fout.write(linea)