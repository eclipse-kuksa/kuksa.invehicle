#!/usr/bin/python3

# Copyright (c) 2018 Eclipse KUKSA project
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0
#
# SPDX-License-Identifier: EPL-2.0
#
# Contributors: Robert Bosch GmbH


import configparser
import sys

import QueryPersonality


personalities = []

destination="/tmp/"

def main(args):
    config = configparser.ConfigParser()
    config.read('config.ini')

    if "General" not in config:
        print("General section missing from configuration, exiting")
        sys.exit(-1)

    general_cfg = config['General']
    hawkbit_server = general_cfg.get('server','localhost:8080')
    destination = general_cfg.get('downloaddir','/tmp')

    print("Will connect to "+str(hawkbit_server))
    print("Will download assets to "+str(destination))


    parse_personalities(config)

    #print(str(personalities))

    if len(personalities) == 0:
        print("No valid personalities configured. Exiting")
        sys.exit(-1)

    for personality in personalities:
        QueryPersonality.queryHawkbit(hawkbit_server,personality,destination)




#Get personalities from config
def parse_personalities(config):
    for section in config:
        if section in [ "DEFAULT", "General"]:
            continue
        print("Got personality "+str(section))
        pers=config[section]
        if "target" not in pers:
            print("Missing target for personality "+str(section))
            continue
        if "securityToken" not in pers:
            print("Missing securityToken for personality " + str(section))
            continue
        personality={}
        personality['target'] = pers['target']
        personality['securityToken'] = pers['securityToken']
        personality['policy'] = pers.get('securityTarget', 'mandatory')
        personalities.append(personality)




if __name__ == "__main__":
    main(sys.argv)
