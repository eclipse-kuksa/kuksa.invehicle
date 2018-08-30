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

import DeployDocker
import DeployCopyStart
import HawkbitUtil

destination="/tmp"



def queryHawkbit(server, personality, dst):
    global destination
    destination=dst

    dd = {}
    dd['personality']=personality
    dd['server']=server 

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
    
    dd['chunks']=r.json()
    downloadChunks(dd)


#We only expect one file, but download all artifacts from all chunks,
#Todo: check what all the Hawkbit parameters mean. Probably Hawkbit can tell us waht we should do and when....
def downloadChunks(dd):
    global destination

    if "deployment" not in dd['chunks']:
        print("No deployment. Aborting")
        return

    deployment=dd['chunks']['deployment']
    if "chunks" not in deployment:
        print("No chunks. Aborting")
        return

    actionId=dd['chunks']['id']
    dd['actionId']=dd['chunks']['id'] #helper functions expect it in top level
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
        targetdir=str(destination)+"/"+str(dd['personality']['target'])
        if not os.path.exists(targetdir):
            os.makedirs(targetdir)

        fname=artifact.get("filename","UNKNOWN")
        dst = targetdir+"/"+fname

        print("Download "+str(url)+" to "+str(dst))
        headers = {'Authorization': 'TargetToken '+dd['personality']['securityToken'], "Content-type" : "application/json" }
        # NOTE the stream=True parameter
        r = requests.get(str(url), stream=True, headers=headers)
        with open(dst, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
            f.flush()


        if (fname.startswith("DOCKER_")):
            print("Carful analysis in extensive checks have revealed this to be a docker image. Yummy")
            DeployDocker.deploy(dst)
        elif (fname.startswith("SIMPLE_")):
            print("Carful analysis in extensive checks have revealed this to be a boring app. Starting anyway")
            DeployCopyStart.deploy(dst)
        else:
            print("Download only")
            
			
		#Give feedback. For now we just say everything is fine
        #data=feedback(dd['server'],actionId, "success")
        HawkbitUtil.feedback(dd, "success");
        #print("Will send "+str(data))
       
        print("Done: "+str(r.status_code))
