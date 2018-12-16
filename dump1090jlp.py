# -*- coding: utf-8 -*-

import requests
import json
import time
import fnmatch
import subprocess

# -----------------------Задаем параметры---------------------

# Файл dump1090 aircraft.json
json_aircrafts = '/mnt/ramdisk/aircraft.json'

# Выборка необходимых позывных
mask_callsign = {
                'RSD*':'В небе Правительственный борт',
                'PSD*':'В небе Правительственный борт',
                'PBD282': 'Кто последний будет улетать из Петрозаводска, выключите в аэропорту свет. Счастливого полета,',
                'PBD281': 'В Петрозаводск понаезжают москвичи рейсом'
                }

# Выборка необходимых HEX
mask_hex = {
                '154*':'В небесах нынче редкая птица Ту-154',
                '14A*':'На радаре Як-42',
                '157710':'Первый на подходе (96016)',
                '157714':'Первый на подходе (96020)',
                '157715':'Первый на подходе (96021)',
                '157716':'Второй на подходе (96022)',
                '3F8518':'Achtung! Luftwaffe в небе!',
                '3F8519':'Achtung! Luftwaffe в небе!',
                '3F8517':'Achtung! Luftwaffe в небе!',
                '3F851A':'Achtung! Luftwaffe в небе!',
                '3F851B':'Achtung! Luftwaffe в небе!',
                '3F7DC1':'Achtung! Luftwaffe в небе!',
                '3F551D':'Achtung! Luftwaffe в небе!',
                '3C6665':'Achtung! Luftwaffe в небе!',
                '3EB1A6':'Achtung! Luftwaffe в небе!',
                '3E89E7':'Achtung! Luftwaffe в небе!',
                '3F4368':'Achtung! Luftwaffe в небе!',
                '0A03F2':'Achtung! Luftwaffe в небе!',
                '3F43D4':'Achtung! Luftwaffe в небе!',
                '3EA1CC':'Achtung! Luftwaffe в небе!',
                '3EA653':'Achtung! Luftwaffe в небе!',
                '3F7001':'Achtung! Luftwaffe в небе!',
                '3F79F9':'Achtung! Luftwaffe в небе!',
                '3F727C':'Achtung! Luftwaffe в небе!',
                '3F7588':'Achtung! Luftwaffe в небе!',
                '3EA556':'Achtung! Luftwaffe в небе!',
                '3F6682':'Achtung! Luftwaffe в небе!',
                '3F6F02':'Achtung! Luftwaffe в небе!',
                '3E8B41':'Achtung! Luftwaffe в небе!',
                '3F5727':'Achtung! Luftwaffe в небе!',
                '3E826F':'Achtung! Luftwaffe в небе!',
                '3F4EFE':'Achtung! Luftwaffe в небе!',
                '3F6931':'Achtung! Luftwaffe в небе!',
                '3F4D0C':'Achtung! Luftwaffe в небе!',
                '3F64F6':'Achtung! Luftwaffe в небе!'
           }

# Через сколько времени считать появление борта новым (секунды)
ttl_max = 3600

# Путь к скрипту, который будет запущен при совпадении масок
script = '/home/denzenarm/bin/./shishkotryas.sh'

# Период сканирования (time to scan)
tts = 30

msg = "Радар ULSS7:"

# -----------------------------------------------------------

# Watched flights
flights_hex = {}
flights_callsign = {}


def check_ttl():
    global flights_hex
    global flights_callsign
    cp_flights_hex = flights_hex.copy()
    cp_flights_callsign = flights_callsign.copy()
    for i in cp_flights_hex:
        ttl = time.time() - cp_flights_hex[i]
        if ttl > ttl_max:
            del flights_hex[i]
    for i in cp_flights_callsign:
        ttl = time.time() - cp_flights_callsign[i]
        if ttl > ttl_max:
            del flights_callsign[i]


def update_dict_hex(hex):
    if hex not in flights_hex:
        flights_hex[hex] = time.time()
        return True
    else:
        return False


def update_dict_callsign(hex):
    if hex not in flights_callsign:
        flights_callsign[hex] = time.time()
        return True
    else:
        return False


def is_valid_jet(hex, callsign):
    for mask in mask_hex:
        if fnmatch.fnmatch(hex, mask):
            if update_dict_hex(hex):
                cmd = '{0} \"{1} {2}, HEX={3}\"'.format(script, msg, mask_hex[mask], hex)
                # print(cmd)
                subprocess.call(cmd, shell = True)
    for mask in mask_callsign:
        if fnmatch.fnmatch(callsign, mask):
            if update_dict_callsign(hex):
                cmd = '{0} \"{1} {2} {3}, HEX={4}\"'.format(script, msg, mask_callsign[mask], callsign, hex)
                # print(cmd)
                subprocess.call(cmd, shell = True)


if __name__ == '__main__':
    while True:
        with open(json_aircrafts) as json_file:
            data = json.load(json_file)
        check_ttl()
        for x in data['aircraft']:
            if 'flight' in x.keys():
                is_valid_jet(x['hex'].upper(), x['flight'].strip())
            else:
                is_valid_jet(x['hex'].upper(), '')
        time.sleep(tts)
