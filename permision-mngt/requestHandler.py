# Copyright (c) 2019 Eclipse Kuksa project
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0
#
# SPDX-License-Identifier: EPL-2.0
#
# Contributors: Robert Bosch GmbH

from json import JSONDecodeError

import tokenStore
import tokenValidator
import keycloakconnector
import json
import configuration

store = tokenStore
auth_url = configuration.getProperty('keycloak', 'url')
realm = configuration.getProperty('keycloak', 'realm')

validator = tokenValidator


def preparePositiveResponse(appID, token, pubkey):
    resp = json.loads('{"appid": "", "token" : ""}')
    resp["appid"] = appID
    resp["token"] = token
    resp["pubkey"] = pubkey
    return json.dumps(resp).encode("utf-8")  # Always return a valid JSON as string


def prepareNegativeResponse(appID, token, pubkey):
    resp = json.loads('{"appid": "", "token" : ""}')
    resp["appid"] = appID
    resp["token"] = token
    resp["pubkey"] = pubkey
    return json.dumps(resp).encode("utf-8")  # Always return a valid JSON as string


def processRequest(request):
    try:
        req_json = json.loads(request)
        api = req_json["api"]
        appID = req_json["appid"]
        secret = req_json["secret"]

    except JSONDecodeError as error:
        print("Json decoding error occurred. The request is not in json format or does not contain the required fields")
        raise SyntaxError
    # check if a valid token is available in the store
    token = None
    isvalid = False
    print('Get token for local store')
    try:
        token = store.getToken(appID, api)
        pubkey = store.getPubKey(appID)
        # Validate the token
        isvalid = validator.isTokenValid(token, pubkey)
        print('Token from store has validity ' + str(isvalid))
    except FileNotFoundError as error:
        print("No token was found for the appID and user combo. SO will try to fetch it from the authorization server.")
        isvalid = False
    except RuntimeError as rError:
        print("Runtime error occurred while retrieving tokens from token store")
        response = prepareNegativeResponse(appID, ' ', ' ')
        return response
    except Exception as exp:
        print("Exception occurred while retrieving token {}".format(exp))
        response = prepareNegativeResponse(appID, ' ', ' ')
        return response
    try:
        if isvalid:
            print('Token from local store is still valid and hence returning it')
            response = preparePositiveResponse(appID, token, pubkey)
            return response
        else:
            # Get token from keycloak
            print('Token form local store is invalid and hence retrieving it from the keycloak server = ' + auth_url)
            keycloak = keycloakconnector.Keycloakconnector(auth_url, realm, appID, secret)
            token = keycloak.getToken(appID, api)
            pubkey = keycloak.getJWTPublickey()
            isvalid = validator.isTokenValid(token, pubkey)
            if isvalid:
                print('Token retrieved from keycloak server is valid so now returning to w3c-server ')
                response = preparePositiveResponse(appID, token, pubkey)
                store.storeToken(appID, api, token)
                store.storePubKey(appID, pubkey)
                return response
            else:
                print('Token retrieved from keycloak server is invalid')
                response = prepareNegativeResponse(appID, token, pubkey)
                return response
    except Exception as exp:
        print("An exception occurred while retrieving token {}".format(exp))
        response = prepareNegativeResponse(appID, " ", " ")
        return response
