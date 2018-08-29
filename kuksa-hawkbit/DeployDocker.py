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

#Experimental docker deployment without magic


import subprocess

def deploy(f):
    print("Trying to deploy docker image in "+str(f))
	# subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None, capture_output=False, shell=False, cwd=None, timeout=None, check=False, encoding=None, errors=None, text=None, env=None)
    # subprocess.call(args, *, stdin=None, stdout=None, stderr=None, shell=False, cwd=None, timeout=None)¶
    reply=""
    try:
	    reply=subprocess.check_output("bzip2 -cd "+str(f)+" | docker load ",shell=True).decode('utf-8')
    except CalledProcessError as cpe:
        print("Error. Return code "+str(cpe.returncode))
        return
    print("Image imported: "+str(reply))
    image_name=reply[reply.index(":")+1:].strip()
    print("Trying to start image "+str(image_name))
    
    ret=subprocess.call("docker run "+image_name,shell=True)
    print("Return code "+str(ret))
