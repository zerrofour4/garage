#!/usr/bin/env python3
from flask import Flask, json, request, jsonify
app = Flask(__name__)

import Adafruit_DHT
import RPi.GPIO as GPIO
import time
from bluepy.btle import Scanner


'''
Pin assignments
'''
RELAY = 21
TEMP = 16

'''
ALlowed btle MAC addresses
'''
TILE_MACS = ['f2:0b:85:9a:76:ef']
SIGNAL_STR = -90
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY, GPIO.OUT)

temp_sensor = Adafruit_DHT.DHT11

def get_temp_humidity():
    humidity = None
    temp = None
    while (humidity is None and temp is None ):
        humidity, temp = Adafruit_DHT.read_retry(temp_sensor, TEMP)
        return { "humidity": humidity, "temp" : temp}


def scan_for_tile():
    scanner = Scanner()
    devices = scanner.scan(3.0)
    if not devices:
        return (True, 0)
    for dev in devices:
        print(dev.addr)
        if dev.addr in TILE_MACS and dev.rssi > SIGNAL_STR:
            return (True, dev.rssi)
    return (True, 0)


@app.route('/garage')
def open():
    stats = {}
    status,rssi = scan_for_tile()
    stats['signal_strength'] = rssi
    print(status)
    if status:
        GPIO.output(RELAY, True)
        time.sleep(.5)
        GPIO.output(RELAY, False)
        stats['action'] = status
    else:
        stats['action'] = status
    stats.update(get_temp_humidity())
    return jsonify(stats)    
    
if __name__ == "__main__":
    run_options = { "host":"0.0.0.0",
                   "port": 80,
                   "debug": False }
    app.run(**run_options)
