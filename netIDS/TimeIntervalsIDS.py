
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
from scapy.all import *
import sys
import binascii
from importlib import reload

if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding("utf-8")

can_data = [0,0,0,0,0,0,0,0,0,0]
dicMsg=[]


class BindClass:
    def __init__(self):

        self.dicMsg = {'can_id': [], 'ts':[], 'len': [], 'byte0':[], 'byte1':[], 'byte2':[], 'byte3':[], 'byte4':[], 'byte5':[], 'byte6':[], 'byte7':[], 'byte8':[]}
        self.prevTimestamp={}
        self.model_normal_behav={}
        self.unique_ids = []

        sqlite_file = 'my_first_db.sqlite'  # name of the sqlite database file
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

        #print(self.ta)
        new_packet = pkt.getlayer(Raw).load
        packet_time = pkt.time
        can_id = bytes(new_packet[0])
        length = len(new_packet)

        for i in range(0,int(length/2)):
            can_msg = bytes(new_packet[i+8])
            hex_byte = binascii.hexlify(can_msg)
            self.dicMsg[str('byte'+str(i))].append(hex_byte)

        can_string = binascii.hexlify(can_id)
        msg_id.append(can_string)

        self.dicMsg['can_id'].append(msg_id)
        self.dicMsg['ts'].append(packet_time)
        self.dicMsg['len'].append(len)

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

        new_packet = pkt.getlayer(Raw).load
        can_id = bytes(new_packet[0])
        packet_time = pkt.time

        can_hex = binascii.hexlify(can_id)
      
        if can_hex in self.model_normal_behav:

            if (((pkt.time - self.prevTimestamp[can_hex]) > 0) & (int(abs(pkt.time - self.prevTimestamp[can_hex]))<int(self.model_normal_behav[can_hex][0]))):
                 has_anomaly = True
                 anomaly_counter += 1
                 file = open("filename", 'a')
                 severityNum=1
                 l2proto="CAN"
                 algorithmName="TimeIntervals"
                 description="CAN ID " + str(can_hex) + " outside the average time interval"
                 self.a=str("CEF:0|RTC-IDS|" + "|{"+str(severityNum)+"}|"+"{"+algorithmName+"}|{"+l2proto+"msg={"+description+"}")
                 #{l2proto}| msg={description} proto={l4Proto} app={l7Proto} smac={srcMac} dmac={dstMac} src={srcIp} dst={dstIp} spt={srcPort} dpt={dstPort} cs1={messageIdentifier} in={messageLength} TrendMicroDsPacketData={messagePayload}
                 self.postprocess()

            self.prevTimestamp[can_hex] = packet_time


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
        
        capture = sniff(iface=interface, prn=cla.buildingModel, stop_filter = lambda x: time.time()-cla.ta >= trainingtime)

        cla.process()

        # testing phase
        if test:

            print("### Testing phase ###\n")

            capture = sniff(iface=interface, prn= cla.anomalyDetection)

            cla.postProcess()


    elif isreal_time==False:
            trainingdata = args[0]
            td = open(trainingdata, "r")

            testingdata = args[1]
            tsd = open(testingdata, "r")

            model = Path("modelFreq")
            if model.is_file():
                print("A model of normal behavior has been found, it will be used as reference of normal behavior\n")
                #anomalyDetection(model,tsd)
            else:
                print("Building first a model of normal behavior...\n")
                #buildingModel(td)
                #anomalyDetection(model,tsd)

            td.close()
            tsd.close()

main()
