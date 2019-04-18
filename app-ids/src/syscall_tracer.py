#!/usr/bin/env python3

# *****************************************************************************
#  Copyright (c) 2018 Fraunhofer IEM and others
#
#  This program and the accompanying materials are made available under the
#  terms of the Eclipse Public License 2.0 which is available at
#  http://www.eclipse.org/legal/epl-2.0
#
#  SPDX-License-Identifier: EPL-2.0
#
#  Contributors: Fraunhofer IEM
# *****************************************************************************



#When contributing, please make sure to stick to PEP8 as much as possible.
#https://www.python.org/dev/peps/pep-0008/

import paho.mqtt.client as mqtt
# needed to call strace
from subprocess import Popen, PIPE, STDOUT
# needed for xml standartized communication
import lxml
import threading  # may use sched instead, using Threading should be non blocking
import logging
from lxml import etree
import psutil

#LOGGING
logger = logging.getLogger("IDS_LOGGER.tracing")
logging.basicConfig(level=logging.DEBUG)

class SyscallTracer(object):
    
    def __init__(self,configpath="./config.xml"):
        
        self.PID =""
        self.PNAME =""
        self.BROKER_IP=""
        self.WINDOW_SIZE=3
        self.bufferlist=[]
        self.CONFIGPATH = configpath
        self.XSD_PATH  = "./xml_validation/configuration_file.xsd"
        self.TRACED_XSD_PATH = "./xml_validation/syscall_tracer_xml.xsd"
        self.client = mqtt.Client()
        self.parse_config(configpath)
        if self.validate_config() != True:
                logging.critical("Configuration invalid.")
                raise SystemExit()

        try:
            self.client.connect(self.BROKER_IP)
        except Exception as e:
            logging.critical("Connection to MQTT Broker failed!\n Exiting program. \n Error: {0}".format(str(e)))
            raise SystemExit(0)

        self.client.loop_start()

        if self.PID != "" and self.PNAME == "":
            self.trace_by_pid()
        elif self.PID =="" and self.PNAME !="":
            self.trace_by_process()
        else:
            logging.error("Either none of PID and PNAME or both got provided.")
            raise SystemExit(1)

    def parse_config(self,configpath):
        from lxml import etree
        root = etree.parse(configpath)
        root = root.getroot()
        for child in root:
            if child.tag == "PID":
                self.PID = child.text
            elif child.tag == "PNAME":
                self.PNAME = child.text
            elif child.tag == "WINDOW_SIZE":
                self.WINDOW_SIZE = int(child.text)
            elif child.tag == "BROKER_IP":
                self.BROKER_IP = child.text
            elif child.tag =="LOGGINGLEVEL":
                if child.text == "INFO":
                    logging.getLogger().setLevel(logging.INFO)
                if child.text == "DEBUG":
                    logging.getLogger().setLevel(logging.DEBUG)
                if child.text == "WARNING":
                    logging.getLogger().setLevel(logging.WARNING)
                if child.text == "CRITICAL":
                    logging.getLogger().setLevel(logging.CRITICAL)
        logging.debug("parse_config: Parsed config with  \nPIDS: {0}\nPNAMES:{1}\nWINDOW SIZE:{2}".format(str(self.PID),str(self.PNAME),str(self.WINDOW_SIZE)))


    def validate_config(self):
        """Uses builtin features to validate the configuration file against the fitting XSD schema"""
        from lxml import etree
        schema = etree.parse(self.XSD_PATH)
        xsd = etree.XMLSchema(schema)

        config = etree.parse(self.CONFIGPATH)
        validity = xsd.validate(config)
        return validity

    def validate_traced_xml(self,XML):
        """Uses lxml validation feature to validate the XML of syscalls against the fitting schema"""
        from lxml import etree
        schema = etree.parse(self.TRACED_XSD_PATH)
        xsd = etree.XMLSchema(schema)

        config = etree.fromstring(XML)
        validity = xsd.validate(config)
        return validity
      
    def find_pids(self):

        import os
        process_ids = []
        try:
            process_ids =  [proc.pid for proc in psutil.process_iter() if proc.name() == self.PNAME]
        except:
            logging.critical("Could not get process IDs to given processname: {0}".format(self.PNAME))
        if len(process_ids) > 0:
            logging.warning("Multiple process IDs with name : '{0}' returned. Using first one.".format(self.PNAME))
            return process_ids[0] 
        else:
            raise ValueError("Could not find a fitting process")

    def trace_by_pid(self):

        proc = Popen(['stdbuf', '-oL', 'strace', '-p',str(self.PID), '-tt'],
                    bufsize=1, stdout=PIPE, stderr=STDOUT, close_fds=True)
        for line in iter(proc.stdout.readline, b''):
            trace = str(line,'utf-8')
            logging.debug("Traced PID" + str(self.PID) + " with trace: \n "+trace)
            self.buffer(trace)
        proc.stdout.close()
        proc.wait()

    def trace_by_process(self):
        self.PID = self.find_pids()
        self.trace_by_pid()

    def buffer(self,trace):

        if "strace" in trace or "Process" in trace:
            return
        if len(self.bufferlist)==self.WINDOW_SIZE:
            self._trace_to_xml(self.bufferlist)
            self.bufferlist = self.bufferlist[1:]
            self.bufferlist.append(trace)
        else:
            self.bufferlist.append(trace)
            
    def publish(self,data,topic):
        if self.client != None:
            self.client.publish(topic, data)
            logging.info("Sucessfully sent:\n" + str(data,"utf-8") + "\nvia Topic 'TRACED'")
        else:
            logging.warning("No MQTT client instantiated!")

    def _trace_to_xml(self, trace_list):
        """Used to first package the data regarding a specific trace
        into an XML-like structure and publishing it via method "publish"
        
        Args:
            processinfo: Processinfo of the traced process. Can be either the PID or a Processname. 
            traces:      List of length of WINDOW_SIZE, contains traces to be packed to XML. 
        """
        dataset = etree.Element("Syscall_Data")
        # create childs of dataset
        pinfo   = etree.SubElement(dataset, "ProcessInfo")
        pinfo.text = str(1)
        traces  = etree.SubElement(dataset, "Syscalls")
        #enumerate over all traces, create a subelement to the traces element with an index for every element
        for trace in trace_list:
            logging.debug(str(trace_list))
            logging.debug("Adding {0}".format(trace))
            trace_xml       = etree.SubElement(traces,"Syscall")
            trace_xml.text  = trace
        # pack to xml string
        data = etree.tostring(dataset, method="xml")
        logging.debug("Parsed to XML\n XML String: \n"+str(data,'utf-8'))
        if self.validate_traced_xml(data):
            self.publish(data, "TRACED")
        else:
            logging.critical("Couldn't validate data: \n{0}".format(data))

        
if __name__ == "__main__":
    SyscallTracer = SyscallTracer("./config.xml")
