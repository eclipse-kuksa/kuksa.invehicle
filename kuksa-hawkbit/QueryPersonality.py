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


import requests
import os.path
import datetime
import json

destination="/tmp"

def feedback(server, actionId, state, stepCurrent=5, stepTo=5, execution="closed", feedback="KUKSA" ): 	
    reply= {}
    reply['id'] = actionId
    reply['time'] = datetime.datetime.utcnow().isoformat()
    reply['status'] = {}
    reply['status']['result'] = {}
    progress= { "of" : stepTo, "cnt": stepCurrent }
    reply['status']['result']['progress']=progress 
    reply['status']['result']['finished']=state 
    reply['status']['execution'] =  execution 
    reply['status']['details'] = [ feedback ]
    
    
    return json.dumps(reply)


def queryHawkbit(server, personality, dst):
    global destination
    destination=dst

    print("Checking assets for device "+str(personality['target']))
    headers = {'Authorization': 'TargetToken '+personality['securityToken'], 'Accept': 'application/hal+json' }
    r = requests.get(server+"/DEFAULT/controller/v1/"+personality['target'], headers=headers)
    if r.status_code != 200:
        print("Invalid status code "+str(r.status_code)+" when querying Hawkbit. Aborting")
        return

    response = r.json()


    #Do we have a deployment base?
    try:
        deploymentbase = response['_links']['deploymentBase']["href"]
    except KeyError:
        print("No deployment base in "+str(response))
        return

    print("Deployment Base is "+str(deploymentbase))

    r = requests.get(str(deploymentbase), headers=headers)
    if r.status_code != 200:
        print("Invalid status accessing deployment base " + str(r.status_code) + " when querying Hawkbit. Aborting")
        return

    response = r.json()
    #print(str(r.json()))
    downloadChunks(server,personality['target'],response, personality)


#We only expect one file, but download all artifacts from all chunks,
#Todo: check what all the Hawkbit parameters mean. Probably Hawkbit can tell us waht we should do and when....
def downloadChunks(server,target,deployment_desc, personality):
    global destination

    if "deployment" not in deployment_desc:
        print("No deployment. Aborting")
        return

    deployment=deployment_desc['deployment']
    if "chunks" not in deployment:
        print("No chunks. Aborting")
        return

    actionId=deployment_desc['id']
    chunks=deployment['chunks']

    for chunk in chunks:
        if "artifacts" not in chunk:
            print("Chunk has no artifacts. Skipping")
            continue
        artifacts = chunk['artifacts']
        for artifact in artifacts:
            try:
                url = artifact["_links"]["download-http"]["href"]
            except KeyError:
                print("No download  source for "+str(artifact))
                return



        #create dir for target
        targetdir=str(destination)+"/"+str(target)
        if not os.path.exists(targetdir):
            os.makedirs(targetdir)

        dst = targetdir+"/"+artifact.get("filename","UNKNOWN")

        print("Download "+str(url)+" to "+str(dst))
        headers = {'Authorization': 'TargetToken '+personality['securityToken'], "Content-type" : "application/json" }
        # NOTE the stream=True parameter
        r = requests.get(str(url), stream=True, headers=headers)
        with open(dst, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
            f.flush()


		#Give feedback. For now we just say everything is fine
        data=feedback(server,actionId, "success")
        #print("Will send "+str(data))
        r = requests.post(server+"/DEFAULT/controller/v1/"+personality['target']+"/deploymentBase/"+actionId+"/feedback", headers=headers, data=data, )
        if r.status_code != 200:
            print("Error reporting state " + str(r.status_code) + " when querying Hawkbit. Aborting")
            print("Response was "+str(r.json()))
            return
   
        print("Done: "+str(r.status_code))
