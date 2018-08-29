from optparse import OptionParser
import time
from flask import Flask, request, g
from flask_restful import Resource, Api
import sqlite3
from scapy.all import *
import sys
import binascii
import numpy as np
from ParentClass import Parentclass

class CANsniffer(Parentclass):


    def __init__(self, name=None):
        Parentclass.__init__(self, name)
        self.ta = 0
        self.counter = 0
        self.unique_ids=[]

    def buildingModel(self, pkt):

        total = 0
        self.counter = self.counter + 1

        if self.counter==1:
            self.ta = time.time()

        msg_id = []

        new_packet = pkt.getlayer(Raw).load
        packet_time = pkt.time
        can_id = new_packet[0]
        length = binascii.hexlify(new_packet[4])

        can_string = binascii.hexlify(can_id)



        if not can_string in self.unique_ids:
            self.unique_ids.append(can_string)
            for i in range(0, int(length)):
                self.dicMsg=np.append({can_string: (np.array([], dtype=str), 0,0)},self.dicMsg)


        for j in range(0, int(length)):


            can_msg = new_packet[j + 8]
            hex_byte = binascii.hexlify(can_msg)

           
            self.counter = self.counter + 1

            if can_string in self.unique_ids:
                if can_string in self.dicMsg[j]:
                    self.dicMsg[j][can_string]= np.append(hex_byte, self.dicMsg[j][can_string])

                


    def process(self):
        counter=-1


        for Id in self.unique_ids:
            counter=counter+1

            for msg in self.dicMsg:
                if Id in msg:
                    self.can_min.append( np.min( msg[Id] ) )
                    self.can_max.append(np.max(msg[Id]))

            min_array = [np.min(int(x)) for x in self.dicMsg]
            
    def postprocess(self):
        try:
            self.c.execute('''CREATE TABLE items (Network, AlertID)''')
        except Exception as e:
            print("table exists")

        self.c.execute("INSERT INTO items (Network, AlertID) VALUES(?,?)", ('lab', self.a))
        self.conn.commit()

    def postprocess2(self):
        self.conn.close()

    def anomalyDetection(self, pkt):

        minTimestamp = 0
        maxTimestamp = 0
        counter = 0


        new_packet = pkt.getlayer(Raw).load
        can_id = new_packet[0]
        length = binascii.hexlify(new_packet[4])

        can_hex = binascii.hexlify(can_id)

        if can_hex in self.unique_ids:
            pos=0
            for j in range(0,len(self.unique_ids)):
                if self.can_byte[j][0] == can_hex:
                    pos=j
            for i in range(0, int(length)):
                can_msg = new_packet[i + 8]
                hex_byte = binascii.hexlify(can_msg)
                if (self.can_byte[pos][i][2]<hex_byte<self.can_byte[pos][i][1]):
                    has_anomaly = True
                    anomaly_counter += 1
                    file = open("filename", 'a')
                    severityNum = 1
                    l2proto = "CAN"
                    algorithmName = "CANpayload"
                    description = "CAN ID " + str(can_hex) + " outside the payload interval"
                    self.a = str("CEF:0|RTC-IDS|" + "|{" + str(
                        severityNum) + "}|" + "{" + algorithmName + "}|{" + l2proto + "msg={" + description + "}")
                    # {l2proto}| msg={description} proto={l4Proto} app={l7Proto} smac={srcMac} dmac={dstMac} src={srcIp} dst={dstIp} spt={srcPort} dpt={dstPort} cs1={messageIdentifier} in={messageLength} TrendMicroDsPacketData={messagePayload}
                    file.write(self.a)
                    file.close()
                    self.postprocess()
        
