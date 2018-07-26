#!/usr/bin/python3

# Copyright (c) 2018 Eclipse KUKSA project
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0
#
# SPDX-License-Identifier: EPL-2.0
#


import requests
import os.path

destination="/tmp"


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
    #print(str(r.json()))


    #Do we have a deployment base?
    try:
        deploymentbase = response['_links']['deploymentBase']["href"]
    except KeyError:
        print("No deployment base in "+str(response))
        print("Aborting")
        return

    print("Deployment Base is "+str(deploymentbase))

    r = requests.get(str(deploymentbase), headers=headers)
    if r.status_code != 200:
        print("Invalid status accessing deployment base " + str(r.status_code) + " when querying Hawkbit. Aborting")
        return

    response = r.json()
    #print(str(r.json()))
    downloadChunks(personality['target'],response, personality)


#We only expect one file, but download all artifacts from all chunks,
#Todo: check what all the Hawkbit parameters mean. Probably Hawkbit can tell us waht we should do and when....
def downloadChunks(target,deployment_desc, personality):
    global destination

    if "deployment" not in deployment_desc:
        print("No deployment. Aborting")
        return

    deployment=deployment_desc['deployment']
    if "chunks" not in deployment:
        print("No chunks. Aborting")
        return

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
        # NOTE the stream=True parameter
        r = requests.get(str(url), stream=True, headers = {'Authorization': 'TargetToken '+personality['securityToken'] })
        with open(dst, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
            f.flush()

        print("Done: "+str(r.status_code))
