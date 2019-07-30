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
import time
import logging

logger = logging.getLogger("IDS_LOGGER.refining")
logging.basicConfig(level=logging.INFO)

class SyscallFormatter(object):
    

    def __init__(self,configpath="./config.xml"):
        try:
            self.CONFIGPATH = configpath
            self.XSD_PATH  = "./xml_validation/configuration_file.xsd"
            self.BROKER_IP = "localhost"
            self.REFINED_XSD_PATH = "./xml_validation/stide_syscall_formatter_xml.xsd"

            self.parse_config()
            if self.validate_config() != True:
                logging.critical("Configuration invalid.")
                raise SystemExit()
            self.client = mqtt.Client()
            self.client.enable_logger(logger=logger)
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.connect(self.BROKER_IP)
            logging.info("Connected to {0}, starting MQTT loop".format(self.BROKER_IP))
            self.client.loop_forever()
        except Exception as e:
            logging.critical("Error initializing SyscallFormatter. See \n {0}".format(str(e)))

    def parse_config(self):
        """Parses the config from CONFIGPATH using the lxml library"""
    
        from lxml import etree
        root = etree.parse(self.CONFIGPATH)
        root = root.getroot()
        for child in root:
            if child.tag == "BROKER_IP":
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
        logging.info("parse_config: Config contains:{0}".format(self.BROKER_IP))

    def validate_config(self):
        """Uses builtin features to validate the configuration file against the fitting XSD schema"""
        from lxml import etree
        schema = etree.parse(self.XSD_PATH)
        xsd = etree.XMLSchema(schema)

        config = etree.parse(self.CONFIGPATH)
        validity = xsd.validate(config)
        return validity

    def validate_refined_xml(self,XML):
        """Uses lxml validation feature to validate the XML of syscalls against the fitting schema"""
        from lxml import etree
        schema = etree.parse(self.REFINED_XSD_PATH)
        xsd = etree.XMLSchema(schema)

        config = etree.fromstring(XML)
        validity = xsd.validate(config)
        return validity

    def on_message(self,client,userdata,msg):
        """MQTT Callback function for handling received messages"""
        # a nice usage of the topic would be to let it transport the PID /
        # Processname
        logging.info("On_Message: Received new message")
        logging.debug("On_Message: New message:\n"+ str(msg.payload))
        from lxml import etree
        xml_string = msg.payload
        root = etree.fromstring(xml_string)
        processinfo = ""
        trace_strings = []
        for child in root:
            logging.debug("On_Message: Processing child:{0}".format(child.tag))
            if child.tag == "ProcessInfo":
                processinfo = child.text
            elif child.tag == "Syscalls":
                logging.debug("On_Message: Processing traces")
                for trace in child:
                    logging.debug("On_Message: Processing trace:{0}".format(trace.text))
                    trace_strings.append(trace.text)
            else:
                logging.debug("On_Message: Nothing to process found in XML:\n {0}".format(str(msg.payload)))

        #messages starting with strace are info / debug / error messages from strace
        
            
        refined_xml = self.parse(trace_strings,processinfo) 
        if self.validate_refined_xml(refined_xml):
            self.publish("REFINED",refined_xml)
        else:
            logging.critical("Couldn't validate data: \n{0}".format(refined_xml))

    
    def on_connect(self,client,userdata,flags,rc):
        logging.info("Connected to broker at {0}".format(self.BROKER_IP) + "with result code {0}".format(rc))
        self.client.subscribe("TRACED") 


    def parse(self,message,processinfo):
        logging.info("parse:  Beginning to parse the message")
        logging.debug("parse:  Parsing: {0} type of param message: {1}".format(message,type(message)))



        traced_strings = message 
        strings_to_send = []
        logging.debug("parse: traced strings are: {0}".format(str(traced_strings)))
        for trace in traced_strings:
            # split the message at the first opened bracket,
            # separating timestamp and syscall from parameters and errorcode
            split_msg = trace.split("(", 1)[0]
            logging.debug("Separated timestamp,syscall from parameters:"+ split_msg)
            #split syscall and timestamp, which are separated by a space
            ts_sys    = split_msg.split(" ",1)
            timestamp = ts_sys[0]  #Timestamp is only used for debugging purposes here
            syscall   = ts_sys[1]
            strings_to_send.append(syscall)
            logging.debug("parse:  Separated timestamp, syscall: "+ timestamp +" " + syscall)
        

        try:
            from lxml import etree
            refined_data = etree.Element("Refined")
            xml_syscalls   = etree.SubElement(refined_data,"Syscalls")
            xml_pinfo     = etree.SubElement(refined_data,"ProcessInfo")
            xml_pinfo.text     = processinfo
            for trace in strings_to_send:
                trace_xml       = etree.SubElement(xml_syscalls,"SYSCALL")
                trace_xml.text  = trace
            logging.debug("parse: Parsing to XML finished.")

            refined = str(etree.tostring(refined_data), 'utf-8')
            logging.info("parse: Parsed refined Data to XML")
            logging.debug("parse: Parsed refined data to XML:\n"+refined)
            return refined
        except Exception as e:
            logging.warning("Error during XML construction: {0}".format(str(e)))

    def publish(self,topic,data):
        """Using the paho mqtt implementation, publish trace on a certain topic."""
        logging.info("Publishing refined message")
        self.client.publish(topic,data)


if __name__ == "__main__":
     SyscallFormatter =  SyscallFormatter("./config.xml")
        
