#!/usr/bin/python3

# Copyright (c) 2018 Eclipse KUKSA project
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0
#
# SPDX-License-Identifier: EPL-2.0
#
# Contributors: Robert Bosch GmbH
#
# This provider gets data from gpsd (http://www.catb.org/gpsd/)

from gps3 import gps3
import sys
import threading
lock=threading.Lock()


position = { "valid":False, "lat":"0", "lon":"0", "alt":"0", "hdop":"0", "speed":"0" }

def loop(gpsd_socket):
    global position,lock
    print("gpsd receive loop started")
    data_stream = gps3.DataStream()
    gpsd_socket.watch()
    for new_data in gpsd_socket:
        if new_data:
            data_stream.unpack(new_data)
            print("GPSD data....")

            lock.acquire()
            position['lat']=data_stream.TPV['lat']
            position['lon']=data_stream.TPV['lon']            
            position['alt']=data_stream.TPV['alt']
            position['speed']=data_stream.TPV['speed']
            if "hdop" in data_stream.SKY:
                position['hdop']=data_stream.SKY['hdop']

            #check if position valid
            if 'n/a' in position.values():
                position['valid']=False
            else:
                position['valid']=True
            lock.release()


def getPosition():
    global position, lock
    lock.acquire()
    p=position
    lock.release()
    return p


def connect(host,port):
    gpsd_socket = gps3.GPSDSocket()
    gpsd_socket.connect(host, port)  #TODO: Find out when it fails

#    loop(gpsd_socket)
    t = threading.Thread(target=loop, args=(gpsd_socket,))
    t.start()
    
def initProvider(config):
    print("Init gpsd provider...")
    if "Provider.gpsd" not in config:
        print("Provider.gpsd section missing from configuration, exiting")
        sys.exit(-1)
    
    provider_config=config['Provider.gpsd']
    gpsd_host=provider_config.get('host','127.0.0.1')
    gpsd_port=provider_config.get('port','2947')

    print("Trying to connect gpsd at "+str(gpsd_host)+" port "+str(gpsd_port))
    connect(gpsd_host,gpsd_port)

    
