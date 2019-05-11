#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = "Jordan Martin"
# __licence__ = "Apache License 2.0"

import serial
import logging
import subprocess
import requests


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

# Port serial
stty_port = '/dev/serial0'

# URL de push vers Jeedom
base_url = 'https://<JEEDOM_HOST>/core/api/jeeApi.php?plugin=virtual&apikey=<API_KEY>&type=virtual&id={}&value={}'

# Clé à récupéré et id de l'info dans Jeedom
measure_keys = {
        'EAST': <XXXX>,
        'SINST1': <YYYY>
}

def main():

    logging.info('Starting...')

    # Reconfigure le port serial pour eviter
    # l'erreur: termios.error: (22, 'Invalid argument')
    logging.info('Reconfigure stty %s' % stty_port)
    subprocess.call(['stty', '-F',  stty_port, 'iexten'])


    with serial.Serial(port=stty_port, baudrate=9600, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE,
                       bytesize=serial.SEVENBITS, timeout=1) as ser:

        logging.info('Reading on %s' % stty_port)

        while True:
            line = ser.readline()
            arr = line.decode('ascii').split('\t')
            
            if len(arr) != 3:
                continue

            send_measure(arr)

def send_measure(arr):

    key = arr[0]

    if key not in measure_keys:
        return False

    if not verify_checksum(arr):
        logging.warn('checksum failure for %s' % key)
        return False

    value = int(arr[1])
    cmd_id = measure_keys.get(key)
    url = base_url.format(cmd_id, value)
    
    logging.info('%s => %s' % (key, value))
    requests.get(url);

    return True


def verify_checksum(arr):
    tag = arr[0]
    data = arr[1]
    checksum = arr[2].replace('\r\n', '')
    checked_data = [ord(c) for c in (tag + '\t' + data + '\t')]
    computed_sum = (sum(checked_data) & 0x3F) + 0x20
    return checksum == chr(computed_sum)

if __name__ == '__main__':
    main()

