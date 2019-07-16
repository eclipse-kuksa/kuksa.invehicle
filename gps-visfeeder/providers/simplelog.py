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
# This provider gets data from a simple log file which contains lines
# formatted 
# lat,lon
# All other values will be reported as 0


import csv
import time
import threading


position = { "valid":False, "lat":"0", "lon":"0", "alt":"0", "hdop":"0", "speed":"0" }

simplelog_interval=1
lock=threading.Lock()

def loop(csv_reader):
    global simplelog_interval,lock
    for line in csv_reader:
        time.sleep(simplelog_interval)
        if not len(line) == 2:
            print("Simplelog skipping invalid line "+str(line))
            continue

        try:
            lat=float(line[0])
            lon=float(line[1])
        except ValueError:
            print("Simplelog skipping invalid line "+str(line))
            continue

        lock.acquire()
        position["lat"]=float(line[0])
        position["lon"]=float(line[1])
        position["valid"]=True
        lock.release()
   
        print("Line is "+str(line))
        
    print("Simplelog: FINISHED")

def initProvider(config):
    global simplelog_interval
    print("Init simplelog provider...")
    if "Provider.simplelog" not in config:
        print("Provider.simplelog section missing from configuration, exiting")
        sys.exit(-1)
    
    provider_config=config['Provider.simplelog']
    simplelog_file=provider_config.get('file','log.csv')
    simplelog_interval=provider_config.getint('interval',1)

    print("Trying to read simeplelog from "+str(simplelog_file)+" with a position every  "+str(simplelog_interval)+" s")

    csv_f=open(simplelog_file)
    csv_reader=csv.reader(csv_f, delimiter=',')
    
    #loop(csv_reader)
    t = threading.Thread(target=loop, args=(csv_reader,))
    t.start()



def getPosition():
    global position, lock
    lock.acquire()
    p=position
    lock.release()
    return p