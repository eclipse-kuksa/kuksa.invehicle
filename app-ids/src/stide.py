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
import sqlite3
import logging
import os


#CONFIGURATION RELEVANT
DB_USER       = ""
DB_PW         = ""
DB_HOST       = "../Traces.sqlite"
CONFIGPATH    = "./config.xml"
BROKER_IP     = "localhost"
STORAGE_MODE  = True
WINDOW_SIZE   = 3
XSD_PATH      = "./xml_validation/configuration_file.xsd"


#NOT CONFIGURATION RELEVANT
DB_CURSOR     = None
DB_CONNECTION = None
logger = logging.getLogger("IDS_LOGGER")
logging.basicConfig(level=logging.DEBUG)

def parse_config():
    """Parses the processer config using lxml"""
    from lxml import etree
    root = etree.parse(CONFIGPATH)
    root = root.getroot()
    global BROKER_IP
    global DB_PW
    global DB_HOST
    global STORAGE_MODE
    global DB_USER
    global WINDOW_SIZE
    for child in root:
        if child.tag == "BROKER_IP":
            BROKER_IP = child.text
        elif child.tag =="DB_PW":
            DB_PW = child.text
        elif child.tag =="DB_HOST":
            DB_HOST = child.text
        elif child.tag=="STORAGE_MODE":
            if child.text == "True":
                STORAGE_MODE=True
            else:
                STORAGE_MODE=False
        elif child.tag =="DB_USER":
            DB_USER=child.text
        elif child.tag =="WINDOW_SIZE":
            WINDOW_SIZE = int(child.text)
        elif child.tag =="LOGGINGLEVEL":
            if child.text == "INFO":
                logging.getLogger().setLevel(logging.INFO)
            if child.text == "DEBUG":
                logging.getLogger().setLevel(logging.DEBUG)
            if child.text == "WARNING":
                logging.getLogger().setLevel(logging.WARNING)
            if child.text == "CRITICAL":
                logging.getLogger().setLevel(logging.CRITICAL)
    
def validate_config():
    """Uses builtin features to validate the configuration file against the fitting XSD schema"""
    from lxml import etree
    schema = etree.parse(XSD_PATH)
    xsd = etree.XMLSchema(schema)

    config = etree.parse(CONFIGPATH)
    validity = xsd.validate(config)
    return validity

def connect_to_db():
    """Used to establish a connection to the database using parameters parsed from configuration file"""
    logging.info("Establishing DB connection")
    dir_path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir_path, DB_HOST)
    path = os.path.normpath(path)
    
    try:
        global DB_CONNECTION
        global DB_CURSOR
        DB_CONNECTION = sqlite3.connect(path)
        DB_CURSOR = DB_CONNECTION.cursor()
        logging.info("Building creation query, creating new table if necessary")
        DB_CURSOR.execute(_build_creation_query(WINDOW_SIZE))
        DB_CONNECTION.commit()
        logging.info("Done.")
    except sqlite3.Error as e:

        logging.critical("Error connecting to DB: {}".format(e.args[0]))


def on_message(client, userdata, msg):
    """Callback function for handling received messages"""
    
    logging.info("on_message: Received new message!")
    logging.debug("on_message: Received {0}".format(str(msg.payload)))
    from lxml import etree
    xml_string = msg.payload
    root = etree.fromstring(xml_string)
    processinfo =""
    timestamp   =""
    syscalls    =[]

    #extract
    for child in root:
        if child.tag == "Timestamp":
            timestamp = child.text
        elif child.tag == "ProcessInfo":
            processinfo = child.text  
        elif child.tag == "Syscalls":
            for call in child:
                syscalls.append(call.text)
    logging.info("on_message: Extracted message")
    if len(syscalls) == WINDOW_SIZE:
        if DB_CONNECTION is not None:
            if STORAGE_MODE == True:
                insert(processinfo,timestamp,syscalls)
            else:
                #STORAGE MODE OFF
                logging.info("on_message: Storage mode off: using STIDE.")
                STIDE(syscalls)
    else:
        raise ValueError("System calls are empty, please check the XML. \n")


def _build_creation_query(windowsize):
    start = "CREATE TABLE IF NOT EXISTS Traces{0} (".format(str(windowsize))
    columns = ""
    primary_keys = ""
    for i in range(0,windowsize):
        columns = columns + "Trace{0} TEXT NOT NULL,".format(str(i))
        primary_keys = primary_keys + "Trace{0},".format(str(i))
    primary_keys = primary_keys[:-1]
    end = "PRIMARY KEY ({0}))".format(primary_keys)
    return start + columns + end 

def _build_insert_query(windowsize):
    """Used to build the insert query depending on the window size"""
    start = "INSERT INTO TRACES{0}(".format(str(windowsize))
    mid   = ""
    for i in range(0,windowsize-1):
        mid = mid + "Trace{0},".format(str(i))
    mid = mid + "Trace{0})".format(str(windowsize-1))
    mid = mid + " VALUES "
    end = "("
    for j in range(0,windowsize-1):
        end = end + "?,"
    end = end + "?)"

    query = start + mid + end 
    return query

def insert(processinfo,timestamp,syscalls):
    """
    Takes processinfo (either PID or PNAME as strings), timestamp as String and syscalls as list of strings as arguments
    """
    logging.info("on_message: Inserting into database")
    logging.debug("on_message: Inserting {0} into database".format(str(syscalls)))
    #build the query depending on window size
    SQL_STATEMENT = _build_insert_query(WINDOW_SIZE)
    try:
        DB_CURSOR.execute(SQL_STATEMENT,tuple(syscalls))
        DB_CONNECTION.commit()
        logging.info("on_message: Insert into DB successfull")
        logging.debug("on_message: Inserted {0} into DB successfully".format(str(syscalls)))
    except Exception as e:
        if isinstance(e,sqlite3.IntegrityError):
            pass
        else:
            logging.critical("Exception during insert, see error message: \n {0}".format(str(e)))


def STIDE(to_compare):
    """sequence time delay embedding:
    Takes an ordered list of system calls. This list is of length WINDOW_SIZE. 
    Gets all fitting datasets from the database and compares accordingly.
    
    Args:
        to_compare: List of length WINDOW_SIZE that contains the ordered systemcalls to compare."""
    logging.debug("Starting STIDE")
    head = to_compare[0]
    SQL = "SELECT * FROM Traces{0} WHERE Trace0 = ?".format(str(WINDOW_SIZE))
    try:
        DB_CURSOR.execute(SQL,(head,))
        db_results = DB_CURSOR.fetchall()
    except Exception as e:
        db_results = []
        logging.critical("Exception during STIDE, couldn't retrieve data from DB. See: \n {0}".format(str(e)))
    if db_results == []:
        publish("ANOMALY","{0} not in DB! Anomaly detected!".format(str(to_compare)))
        logging.info("Database is empty.")
        return
    else:
        match_found = False
        for x_tupel in db_results:
            calls = list(x_tupel)
            if to_compare == calls:
                match_found = True
        if match_found == False:
            publish("ANOMALY","{0} not in DB! Anomaly detected!".format(str(to_compare)))
            logging.info("Database is not empty, but no match for {0} is found.".format(str(to_compare)))
            


def on_connect(client, userdata, flags, msg):
    connect_to_db()
    logging.info("on_connect: Connected to DB!")
    client.subscribe("REFINED")
    logging.info("on_connect: Subscribed to 'REFINED' ")

def publish(topic, data):
    """Using the paho mqtt implementation, publish trace on a certain topic."""
    logging.info("Publishing message {0}".format(data))
    client.publish(topic,data)

def publish_anomaly(db_trace,trace,index):
    msg = "Found anomaly at index {0}. \n DB TRACE: {1}. \n TRACE: {2} \n".format(str(index),str(db_trace),str(trace))
    logging.info(msg)
    publish("ANOMALY",msg)


def compare(a,b):
    """Compares two lists element-wise, logs mismatches.
    Args:
        a: First list  (should be from the database set)
        b: Second list (should be from the tracing module)
    """
    logging.debug("Comparing {0} to {1}".format(str(a),str(b)))
    if len(a) == len(b):
        logging.debug("Checking {0} against {1}".format(str(a),str(b)))
        for index in range(len(a)):
            if a[index] != b[index]:
                logging.warning("Mismatch detected at index {0}. \n DB Trace: {1} \n To compare: {2}".format(str(index),str(a),str(b)))
                publish_anomaly(a,b,index)
            else:
                logging.debug("DB Trace:{0} \n Trace:{1} matched".format(str(a),str(b)))


client = mqtt.Client()
parse_config()
if validate_config() != True:
    logging.critical("Configuration invalid.")
    raise SystemExit()
client.on_connect = on_connect
client.on_message=on_message
logging.info("Connecting to BROKER {0}".format(BROKER_IP))
client.connect(BROKER_IP)
client.loop_forever()
