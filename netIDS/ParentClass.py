from optparse import OptionParser
import time
import sqlite3
import threading
from scapy.all import *
import sys
import binascii
import numpy as np
from abc import ABCMeta, abstractmethod


MAX=12232334



class Parentclass(object, metaclass=ABCMeta):

    def __init__(self, name=None):
        if name:
            self.name = name


        self.dicMsg = []

        self.unique_ids = []
        self.counter = 1
        self.can_min = [MAX] * 1000
        self.can_max = [0] * 1000
        sqlite_file = 'CANalerts.sqlite'  # name of the sqlite database file
        self.conn = sqlite3.connect(sqlite_file)
        self.conn.text_factory = str
        self.c = self.conn.cursor()

        try:
            self.c.execute('''CREATE TABLE items (Network, AlertID)''')
        except Exception as e:
            print("table exists")

        for i in range(8):
            self.dicMsg.append(np.array([], dtype=str))

    @staticmethod
    def factory_method(interface):

        from sniffer.CANPayloadRealTime import CANsniffer
        from sniffer.WiFiClass import Wifisniffer
        if "can" in interface:
            return CANsniffer()
        elif "eth" in interface or "wlan":
            return Wifisniffer()
        else:
            return None


    @abstractmethod
    def buildingModel(self,pkt):

        raise NotImplementedError("not implemented")

    @abstractmethod
    def process(self):

        raise NotImplementedError("not implemented")

    @abstractmethod
    def postprocess(self):

        raise NotImplementedError("not implemented")

    def postprocess2(self):
        self.conn.close()

        # Anomaly detection

    @abstractmethod
    def anomalyDetection(self, pkt):
        raise NotImplementedError("not implemented")

if __name__ == '__main__':
    usage = "usage: %prog [options] <trainingdata> <testingdata>"
    parser = OptionParser(usage=usage)

    (options, args) = parser.parse_args()
    interface = str(args[1])

    cla=Parentclass.factory_method(interface)
    p = Process(target=runProcess, args=())
    p.daemon = True
    p.start()


    isreal_time=True

    if args[2]:
        test = args[2]
    else:
        test = False

    if isreal_time==True:
        trainingtime=float(args[0])

        print("### Training phase ###\n")
        capture = sniff(iface=interface, prn=cla.buildingModel, stop_filter = lambda x: time.time()-cla.ta >= trainingtime)
        cla.process()

        if test:


            print("### Testing phase ###\n")


            capture = sniff(iface=interface, prn= cla.anomalyDetection)


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


