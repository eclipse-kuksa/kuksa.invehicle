
#!/usr/bin/python3

# Copyright (c) 2018 SecurityMatters
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0
#
# SPDX-License-Identifier: EPL-2.0
#
# Contributors: Alexios Lekidis (alexios.lekidis@secmatters.com)
#

import sys, getopt
from optparse import OptionParser
import time
from pathlib import Path
import sqlite3
from rawSniffer import sniff
import sys
from importlib import reload
from bitstring import BitStream

if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding("utf-8")

dicMsg=[]


class BindClass:
    def __init__(self):

        self.dicMsg = {'can_id': [], 'ts':[], 'len': []}
        self.prevTimestamp={}
        self.model_normal_behav={}
        self.unique_ids = []

        sqlite_file = 'EventDB.sqlite'  # sqlite database file
        self.conn = sqlite3.connect(sqlite_file)
        self.conn.text_factory = str
        self.c = self.conn.cursor()
        self.counter=0
        self.ta=0

    def buildingModel(self,pkt):

        msg_id=[]

        total = 0
        self.counter = self.counter + 1

        if self.counter==1:
            self.ta = time.time()

        new_packet = pkt.data
        packet_time = pkt.time
        can_packet = bytes(new_packet)
        stream=BitStream(can_packet)
        can_string=stream.read(8).hex
        length = len(new_packet)

        msg_id.append(can_string)

        self.dicMsg['can_id'].append(msg_id)
        self.dicMsg['ts'].append(packet_time)
        self.dicMsg['len'].append(length)

        self.prevTimestamp.update({msg_id[0]: 0})

        if not msg_id in self.unique_ids:
            self.unique_ids.append(msg_id)

    def process(self):
        for id in self.unique_ids:
            tsnew = 0
            tsold = 0
            timestamp=[]
            mean=[]
            for i in range(1,len(self.dicMsg['can_id'])):
                if id == self.dicMsg['can_id'][i]:
                    tsnew = self.dicMsg['ts'][i]
                    # store the wait time (=the time difference between 2 occurences of the CAN ID)
                    if tsold != 0:
                        timestamp.append(tsnew - tsold)
                    tsold = tsnew
            if timestamp!=[]:
                mean.append(sum(timestamp) / len(timestamp))
                self.model_normal_behav.update({id[0]:mean})

    def postprocess(self):
        try:
            self.c.execute('''create table items (Network, AlertID)''')
        except Exception as e:
            print("table exists")

        self.c.execute("INSERT INTO items (Network, AlertID) VALUES(?,?)", ('lab',self.a))
        self.conn.commit()

    def postprocess2(self):
        self.conn.close()

    #Anomaly detection
    def anomalyDetection(self,pkt):

        new_packet = pkt.data
        packet_time = pkt.time
        anomaly_counter = 0

        can_packet = bytes(new_packet)
        stream=BitStream(can_packet)
        can_string=stream.read(8).hex

        if can_string in self.model_normal_behav:

            if (((pkt.time - self.prevTimestamp[can_string]) > 0) & (int(abs(pkt.time - self.prevTimestamp[can_string]))<int(self.model_normal_behav[can_string][0]))):
                 anomaly_counter += 1
                 file = open("filename", 'a')
                 severityNum=1
                 l2proto="CAN"
                 algorithmName="TimeIntervals"
                 description="CAN ID " + can_string + " outside the average time interval"
                 self.a=str("CEF:0|RTC-IDS|" + "|{"+str(severityNum)+"}|"+"{"+algorithmName+"}|{"+l2proto+"msg={"+description+"}")
                 self.postprocess()

            self.prevTimestamp[can_string] = packet_time


def main():

    if __name__ == '__main__':
       usage = "usage: %prog [options] <trainingdata> <testingdata>"
       parser = OptionParser(usage=usage)

       (options, args) = parser.parse_args()
       interface = str(args[1])

       cla=BindClass()


    isreal_time=True
    if args[2]:
        test = args[2]
    else:
        test = False

    if isreal_time==True:

        # training phase
        trainingtime=float(args[0])

        print("### Training phase ###\n")

        capture = sniff().sniff_online(iface=interface, prn=cla.buildingModel, stop_function = lambda x: time.time()-cla.ta >= trainingtime)

        cla.process()

        # testing phase
        if test:

            print("### Testing phase ###\n")

            capture = sniff().sniff_online(iface=interface, prn= cla.anomalyDetection)

            cla.postProcess()

main()
