#!/usr/bin/env python3
from flask import Flask, json, request, jsonify
app = Flask(__name__)

from elasticsearch import Elasticsearch
import Adafruit_DHT
import RPi.GPIO as GPIO
import time


'''
Pin assignments
'''
RELAY = 21
TEMP = 16

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY, GPIO.OUT)

temp_sensor = Adafruit_DHT.DHT11

es = Elasticsearch("192.168.1.111:9200")

def _post_to_es(doc):
    res = es.index(index="weather", body=doc)
    return res
    
    

def get_temp_humidity():
    humidity = None
    temp = None
    while (humidity is None and temp is None ):
        humidity, temp = Adafruit_DHT.read_retry(temp_sensor, TEMP)
        return { "humidity": humidity, "temp" : temp,
                 "timestamp": int(time.time()),
                 "location": "garage" }



@app.route('/garage')
def open():
    stats = dict()
    GPIO.output(RELAY, True)
    time.sleep(.5)
    GPIO.output(RELAY, False)
    stats.update(get_temp_humidity())
    _post_to_es(stats)
    return jsonify(stats)    
    
if __name__ == "__main__":
    run_options = { "host":"0.0.0.0",
                   "port": 8000,
                   "debug": False }
    app.run(**run_options)


