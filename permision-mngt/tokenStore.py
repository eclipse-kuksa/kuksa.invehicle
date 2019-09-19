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
    logging.info("Token retrieved from storage for " + appid)
    return token


def storeToken(appid, api, token):
    if not os.path.exists(directory):
        os.makedirs(directory)
    path = directory + '/' + appid + api
    f = open(path, "w")
    f.write(token)
    f.close()
    logging.info("Token stored in storage for " + appid)


def getPubKey(appid):
    if not os.path.exists(directory):
        os.makedirs(directory)
    path = directory + '/' + appid + 'pubkey'
    f = open(path, "r")
    pubkey = f.read()
    f.close()
    logging.info("Pubkey retrieved from storage for " + appid)
    return pubkey


def storePubKey(appid, pubkey):
    if not os.path.exists(directory):
        os.makedirs(directory)
    path = directory + '/' + appid + 'pubkey'
    f = open(path, "w")
    f.write(pubkey)
    f.close()
    logging.info("Pubkey stored in storage for " + appid)
