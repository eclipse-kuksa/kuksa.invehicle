# Copyright (c) 2019 Eclipse Kuksa project
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0
#
# SPDX-License-Identifier: EPL-2.0
#
# Contributors: Robert Bosch GmbH

# This files handles the secure storage of the token.
import logging
import os

directory = 'store'


def getToken(appid, api):
    if not os.path.exists(directory):
        os.makedirs(directory)
    path = directory + '/' + appid + api
    f = open(path, "r")
    token = f.read()
    f.close()
    logging.info("Token retrieved in storage for " + appid)
    return token


def storeToken(appid, api, token):
    if not os.path.exists(directory):
        os.makedirs(directory)
    path = directory + '/' + appid + api
    f = open(path, "w")
    f.write(token)
    f.close()
    logging.info("Token stored in storage for " + appid)
