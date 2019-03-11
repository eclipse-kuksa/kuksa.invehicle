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

from socket import socket, AF_PACKET, SOCK_RAW, SOL_SOCKET, SO_RCVBUF, htons
import struct
from fcntl import ioctl


ETH_P_ALL = 3
SIOCGIFINDEX   = 0x8933
SIOCGSTAMP     = 0x8906

SOL_PACKET = 263

MTU = 0xffff


class pktStruct():
    def __init__(self, field1, field2):
        self.data = field1
        self.time = field2

# Class for reading layer 2 packets using Linux PF_PACKET sockets

class ListeningSocket():
    def __init__(self, iface = None, type = ETH_P_ALL, promisc=None, filter=None, nofilter=0):
        self.type = type
        self.outs = None
        self.ins = socket(AF_PACKET, SOCK_RAW, htons(type))
        self.ins.setsockopt(SOL_SOCKET, SO_RCVBUF, 0)
        if iface is not None:
            self.ins.bind((iface, type))
        
        self.promisc = promisc

        if isinstance(iface, list):
            self.iff = iface
        else:
            self.iff = [iface]
        if self.promisc:
            for i in self.iff:
                set_promisc(self.ins, i)
        self.ins.setsockopt(SOL_SOCKET, SO_RCVBUF, 2**30)
    
    def close(self):
        if self.promisc:
            for i in self.iff:
                set_promisc(self.ins, i, 0)
        if hasattr(self, "outs"):
            if not hasattr(self, "ins") or self.ins != self.outs:
                if self.outs and self.outs.fileno() != -1:
                    self.outs.close()
        if hasattr(self, "ins"):
            if self.ins and self.ins.fileno() != -1:
                self.ins.close()

    def recv(self, x=MTU):

        sniffed_bytes, _ = self.ins.recvfrom(x)

        pkt_time = get_packet_timestamp(self.ins)

        pkt = pktStruct(sniffed_bytes, pkt_time)

        return pkt


# Class for reading layer 2 packets using Linux PF_PACKET sockets

class sniff:

    def __init__(self, iface = None, type = ETH_P_ALL, promisc=None, filter=None, nofilter=0):
        self.type = type
        self.outs = None
        self.ins = socket(AF_PACKET, SOCK_RAW, htons(type))
        self.ins.setsockopt(SOL_SOCKET, SO_RCVBUF, 0)
        if iface is not None:
            self.ins.bind((iface, type))

        self.promisc = promisc
        if isinstance(iface, list):
            self.iff = iface
        else:
            self.iff = [iface]
        if self.promisc:
            for i in self.iff:
                set_promisc(self.ins, i)
        self.ins.setsockopt(SOL_SOCKET, SO_RCVBUF, 2**30)

    def sniff_online(self, prn=None, L2socket=None, timeout=None,
              stop_function=None, iface=None, *arg, **karg):

        sniff_sockets = {}  # socket: label dict

        if not sniff_sockets or iface is not None:
            if isinstance(iface, list):
                sniff_sockets.update(
                    (ListeningSocket(type=ETH_P_ALL, iface=ifname, *arg, **karg), ifname)
                    for ifname in iface
                )
           
            else:
                sniff_sockets[ListeningSocket(type=ETH_P_ALL, iface=iface,
                                       *arg, **karg)] = iface
        try:
            while sniff_sockets:
                for key, _ in sniff_sockets.items():
                    try:
                        p = key.recv()
                    except Exception as e:
                        print(e)
                        continue
                    if p is None:
                        del sniff_sockets[s]
                        break
                    if prn is not None:
                        r = prn(p)
                        if r is not None:
                            print(r)
                    if stop_function is not None and stop_function(p):
                        sniff_sockets = {}
                        break

        except KeyboardInterrupt:
            pass


def set_promisc(s,iff,val=1):
        mreq = struct.pack("IHH8s", get_if_index(iff), 1, 0, b"")
        if val:
            cmd = 1
        else:
            cmd = 2
        s.setsockopt(SOL_PACKET, cmd, mreq)

def get_packet_timestamp(sock):
        ts = ioctl(sock, SIOCGSTAMP, "1234567890123456")
        s,us = struct.unpack("QQ",ts)
        return s+us/1000000.0

def get_if_index(iff):
    return int(struct.unpack("I",get_if(iff, SIOCGIFINDEX)[16:20])[0])

def get_if(iff, cmd):
    """Ease SIOCGIF* ioctl calls"""

    sck = socket()
    ifreq = ioctl(sck, cmd, struct.pack("16s16x", iff.encode("utf8")))
    sck.close()
    return ifreq

