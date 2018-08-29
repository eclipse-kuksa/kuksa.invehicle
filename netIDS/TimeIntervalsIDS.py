
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

#from typing import List, Any

from optparse import OptionParser
import time
from pathlib import Path
import sqlite3
from scapy.all import *
import sys
import binascii
from importlib import reload


reload(sys)
if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding("utf-8")

can_data = [0,0,0,0,0,0,0,0,0,0]
dicMsg=[]



    #self.c.execute("CREATE TABLE {tn} ({nf} {ft})"\
     #               .format(tn=table_name1, nf=alert, ft=field_type))
    # Perform query and return JSON data
    #query = conn.execute("select distinct DEPARTMENT from salaries")
    #conn.commit()
    #conn.close()

def getdb():
     DATABASE = 'my_first_db.sqlite'
     db = getattr(g, '_database', None)
     if db is None:
         db = g._database = sqlite3.connect(DATABASE)
         db.text_factory = str
     return db


        #with app.open_resource('my_first_db.sqlite', mode='r') as f:
        #  db.cursor().executescript(f.read())
      #db.commit()

   #app.run()

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

        #self.thread1 = myThread(1, "Thread-1", 1)
        #self.thread1.daemon = True
        #self.thread1.start()

        #self.c.execute('CREATE TABLE {tn} ({nf} {ft})' \
         #         .format(tn=table_name1, nf=new_field, ft=field_type))


    def buildingModel(self,pkt):

        total = 0
        #self.ta = time.time()
        #To calculate the total duration of the data capture.
        #We will save the first and last timestamps and substract them to each other.
        minTimestamp = 0
        maxTimestamp = 0


        msg_id=[]

        total = 0
        self.counter = self.counter + 1

        if self.counter==1:
            self.ta = time.time()

        #print(self.ta)
        new_packet = pkt.getlayer(Raw).load
        #new_packet1=str(new_packet1)
        #new_packet1=new_packet
        #print (new_packet)
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



        #self.c.execute("CREATE TABLE {tn} ({nf} {ft})"\
         #               .format(tn=table_name1, nf=alert, ft=field_type))
        # Perform query and return JSON data
        #query = conn.execute("select distinct DEPARTMENT from salaries")
        #conn.commit()
        #conn.close()

    def postprocess2(self):
        self.conn.close()

    #Anomaly detection
    def anomalyDetection(self,pkt):
        #print("### Testing phase ###\n")

        minTimestamp = 0
        maxTimestamp = 0
        counter=0

        # for line in model:
        #     #pieces = line.split(' ')
        #     canid = model['can_id'][counter]
        #     frameTime=model['ts'][counter]
        #     frameLength=model['len'][counter]
        #     counter=counter+1


        #model.seek(0, 0)

        has_anomaly = False
        anomaly_counter = 0


        #dicMsg = {}
        #Format of the dictionary: {'CAN ID': [counter, last timestamp] }
        #for canid in model_normal_behav:
            #an alert will be raised every three consecutive anomalies
        #    dicMsg[canid] = [0, 0]

        dos_threshold = 1 #number of packets seen with time interval < 0.2 ms to raise a DOS attack alert
        dos_counter = 0

        new_packet = pkt.getlayer(Raw).load
        can_id = bytes(new_packet[0])
        packet_time = pkt.time

        can_hex = binascii.hexlify(can_id)
        # for line in tsd:
        #     msg = SFFMessage(line)
        if can_hex in self.model_normal_behav:
        #         #In the paper they do not discussed how to handle unforeseen IDs
        #     dicMsg[msg.id][0] += 1
        #     if dicMsg[msg.id][0] == 1: #if this is the first time we see this ID
        #         dicMsg[msg.id][1] = msg.ts
        #         continue
            if (((pkt.time - self.prevTimestamp[can_hex]) > 0) & (int(abs(pkt.time - self.prevTimestamp[can_hex]))<int(self.model_normal_behav[can_hex][0]))):
                 has_anomaly = True
                 anomaly_counter += 1
                 file = open("filename", 'a')
                 severityNum=1
                 l2proto="CAN"
                 algorithmName="TimeIntervals"
                 #can_string=int(can_id, 16)
                 description="CAN ID " + str(can_hex) + " outside the average time interval"
                 self.a=str("CEF:0|RTC-IDS|" + "|{"+str(severityNum)+"}|"+"{"+algorithmName+"}|{"+l2proto+"msg={"+description+"}")
                 #{l2proto}| msg={description} proto={l4Proto} app={l7Proto} smac={srcMac} dmac={dstMac} src={srcIp} dst={dstIp} spt={srcPort} dpt={dstPort} cs1={messageIdentifier} in={messageLength} TrendMicroDsPacketData={messagePayload}
                 file.write(self.a)
                 file.close()
                 #print("Injection attack ! CAN ID", pkt.id)
                 self.postprocess()
                 #self.postprocess(sa)

            # if abs(pkt.time - self.prevTimestamp[can_id]) < 0.0002:
            #      dos_counter += 1
            #      if dos_counter == dos_threshold:
            #          print("DOS attack detected")
            #          dos_counter = 0

            self.prevTimestamp[can_hex] = packet_time



        #
        # print("\n### Summary ###\n")
        # if not has_anomaly:
        #     print("Analysis done: no anomaly has been found.")
        # else:
        #     if anomaly_counter==1:
        #         print("One anomaly has been found !")
        #     else:
        #         print("{0:d} anomalies have been found !\n".format(anomaly_counter))


def main():

    if __name__ == '__main__':
       usage = "usage: %prog [options] <trainingdata> <testingdata>"
       parser = OptionParser(usage=usage)

       (options, args) = parser.parse_args()
       interface = str(args[1])

       cla=BindClass()


    #e = create_engine('sqlite:///salaries.db')

    #thread1 = myThread(1, "Thread-1", 1)
    #thread1.daemon = True
    #thread1.start()


    isreal_time=True
    if args[2]:
        test = args[2]
    else:
        test = False

    if isreal_time==True:
        trainingtime=float(args[0])
        #ta=time.time()


        # learning_phase
        #while ((tb-ta)<=trainingtime):

            #capture=sniff(iface="enp0s31f6", filter="host 127.0.0.1 and port 1337")
        print("### Training phase ###\n")
        #while (time.time() - cla.ta > trainingtime):
        capture = sniff(iface=interface, prn=cla.buildingModel, stop_filter = lambda x: time.time()-cla.ta >= trainingtime)
        print("Came from here")

        cla.process()

        #if ~capture:
        #    break

        # training phase
        if test:

        # capture=sniff(iface="enp0s31f6", filter="host 127.0.0.1 and port 1337")
        # learning_phase
        #args[0]+++
        # training phase
            print("### Testing phase ###\n")


            capture = sniff(iface=interface, prn= cla.anomalyDetection)

            cla.postProcess()
            #cla.postProcess2()
            #if ~capture:
            #    break


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


#def pkt_callback(pkt):


#    can_data=[]

#    new_packet=pkt.getlayer(Raw).load
#    packet_time=pkt.time
#    can_id=new_packet[0]
#    len=new_packet[4]
#    can_data[0]=new_packet[8]

#    return
main()
