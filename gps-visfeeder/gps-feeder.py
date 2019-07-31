#!/usr/bin/python3

# Copyright (c) 2019 Eclipse KUKSA project
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0
#
# SPDX-License-Identifier: EPL-2.0
#
# Contributors: Robert Bosch GmbH
#

import sys
import configparser
import importlib
import time
from providers import *
from os import path
from datetime import datetime

import websocket
try:
    import thread
except ImportError:
    import _thread as thread

import json
import random
import ssl

config_candidates=['gps-feeder.ini', '/etc/gps-feeder.ini']
location_provider='gpsd'
config=''
publishing_interval=1


def instantiateProvider(provider, config):
    mod=importlib.import_module("providers."+provider)
    mod.initProvider(config)
    return mod
    

def main(args):
    global location_provider
    global config
    global publishing_interval

    config = configparser.ConfigParser()
    configfile=None

    for candidate in config_candidates:
        if path.isfile(candidate):
            configfile=candidate
            break
    if configfile is None:
        print("No configuration file found. Exiting")
        sys.exit(-1)


    print("Reading configuration from "+str(configfile))
    config.read(configfile)

    if "w3cserver" not in config:
        print("Traccar section missing from configuration, exiting")
        sys.exit(-1)

    w3cserver_cfg = config['w3cserver']
    w3c_server              = w3cserver_cfg.get('server','localhost:8090')
    publishing_interval = w3cserver_cfg.getint('interval',30)

    if "Provider" not in config:
        print("Provider section missing from configuration, exiting")
        sys.exit(-1)

    provider_cfg = config['Provider']
    location_provider = provider_cfg.get('provider','gpsd')

    print("Will connect to "+str(w3c_server))
    print("Will publish location every "+str(publishing_interval))
    

    print("Location data will be provided by "+str(location_provider))
    # Websocket connection with w3c server
    ws = websocket.WebSocketApp("wss://localhost:8090/vss",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})



def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("WebSocket connection open.")
    print("Sending authenticate request.")
    rid = random.randint(1,999999)
    pythonDictionary = {"action": "authorize",  "requestId": rid, "tokens": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJFeGFtcGxlIEpXVCIsImlzcyI6IkVjbGlwc2Uga3Vrc2EiLCJhZG1pbiI6dHJ1ZSwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE2MDkzNzI4MDB9.lxYf-N0C66NgJiinrY_pgVpZOxgH0ppnbMsdKfNiQjbMqYTY_nEpXufmjquvBaxiYsRb_3ScXA__gmviWj_PQoU3apuMVxJjAY6xrwaXFw7g-daUi21yqLSfLptH2vqQzhA_Y1LU6u7SjeiEcGRZrgq_bHnjMM61EVDSnKGCClo"}
    dictionaryToJson = json.dumps(pythonDictionary)
    ws.send(dictionaryToJson.encode('utf8'))
#    time.sleep(1)
    
    def run(*args):
        
        print("Trying to instantiate "+str(location_provider)+" provider")
        provider=instantiateProvider(location_provider,config)
         # start sending messages every second ..
        while True:
            pos=provider.getPosition()
            print("Current pos "+str(pos))
            if pos['valid']:
               rid = random.randint(1,999999)
               lat = pos['lat']
               lon = pos['lon']
               
               latDict = {'Latitude' : lat}
               lonDict = {'Longitude' : lon}
               values = [latDict , lonDict]
               pythonDictionary = {"action": "set",  "requestId": rid, "path": "Signal.Cabin.Infotainment.Navigation.CurrentLocation.*"}
               pythonDictionary.update(value = values) 
               dictionaryToJson = json.dumps(pythonDictionary)
               ws.send(dictionaryToJson.encode('utf8'))
            else:
               print("No valid position. Not posting")
            time.sleep(publishing_interval)
    thread.start_new_thread(run, ())


if __name__ == "__main__":
   main('')   
