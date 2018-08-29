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


class Wifisniffer(Parentclass):

    def __init__(self, name=None):
        Parentclass.__init__(self, name)
        self.ta=0
        self.counter = 0
        self.unique_src = []
        self.unique_dst = []

        self.l4Proto = []

    def buildingModel(self, pkt):

        total = 0

        if self.counter==1:
            self.ta = time.time()

        msg_id = []

        try:
            new_packet = pkt.getlayer(Ether).load

            if pkt.src not in self.unique_src:
                self.unique_src.append(pkt.src)
            if pkt.dst not in self.unique_dst:
                self.unique_dst.append(pkt.dst)

            eth_type = hex(pkt.type)

            if eth_type == "0x8947":
                if "GeoNetworking" not in self.l4Proto:
                    self.l4Proto.append("GeoNetworking")
                self.counter = self.counter + 1
            elif eth_type == "0x6e72":
                if "Automotive Lab" not in self.l4Proto:
                    self.l4Proto.append("Automotive Lab")
                self.counter = self.counter + 1
            else:
                if "None" not in self.l4Proto:
                    self.l4Proto.append("None")

        except:
            print("No ethernet layer")



    def process(self):
        counter=-1


    def postprocess(self):

        self.c.execute("INSERT INTO items (Network, AlertID) VALUES(?,?)", ('lab', self.a))
        self.conn.commit()

    def postprocess2(self):
        self.conn.close()

    def anomalyDetection(self, pkt):

        try:
            new_packet = pkt.getlayer(Ether).load
            severityNum = 1
            algorithmName="V2Xdetection"
            eth_type = hex(pkt.type)

            if (pkt.src not in self.unique_src):

                description = "Src IP" + str(pkt.src) + " outside the whitelist IPs list"
                self.a = str("CEF:0|RTC-IDS|" + "|{" + str(
                    severityNum) + "}|" + "{" + algorithmName + "}|{ msg={" + description + "}")
            elif (pkt.dst not in self.unique_dst):
                description = "Dst IP" + str(pkt.dst) + " outside the whitelist IPs list"
                self.a = str("CEF:0|RTC-IDS|" + "|{" + str(
                    severityNum) + "}|" + "{" + algorithmName + "}|{ msg={" + description + "}")
            self.postprocess()


        except:
            print("No ethernet layer")
