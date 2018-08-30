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
#

import json
import requests
import datetime

def feedback(dd, state, stepCurrent=5, stepTo=5, execution="closed", feedback="KUKSA" ):
    headers = {'Authorization': 'TargetToken '+dd['personality']['securityToken'], "Content-type" : "application/json" }
    reply= {}
    reply['id'] = dd['actionId']
    reply['time'] = datetime.datetime.utcnow().isoformat()
    reply['status'] = {}
    reply['status']['result'] = {}
    progress= { "of" : stepTo, "cnt": stepCurrent }
    reply['status']['result']['progress']=progress 
    reply['status']['result']['finished']=state 
    reply['status']['execution'] =  execution 
    reply['status']['details'] = [ feedback ]

    r = requests.post(dd['server']+"/DEFAULT/controller/v1/"+dd['personality']['target']+"/deploymentBase/"+dd['actionId']+"/feedback", headers=headers, data=json.dumps(reply) )
    if r.status_code != 200:
        print("Error reporting state " + str(r.status_code) + " when querying Hawkbit. Aborting")
        print("Response was "+str(r.json()))
        return

    return
