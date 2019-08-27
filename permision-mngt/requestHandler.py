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

store = tokenStore
auth_url = "http://localhost:8080/auth/"
realm = "Kuksa"


validator = tokenValidator


def preparePositiveResponse(appID, token):
    resp = json.loads('{"appid": "", "token" : ""}')
    resp["appid"] = appID
    resp["token"] = token
    return json.dumps(resp).encode("utf-8")  # Always return a valid JSON as string


def prepareNegativeResponse(appID, token):
    resp = json.loads('{"appid": "", "token" : ""}')
    resp["appid"] = appID
    resp["token"] = token
    return json.dumps(resp).encode("utf-8")  # Always return a valid JSON as string


def processRequest(request):
    try:
        req_json = json.loads(request)
        api = req_json["api"]
        appID = req_json["appid"]
        secret = req_json["secret"]
        keycloak = keycloakconnector.Keycloakconnector(auth_url, realm, appID, secret)
    except JSONDecodeError as error:
        print("Json decoding error occurred. The request is not in json format or does not contain the required fields")
        raise SyntaxError
    # check if a valid token is available in the store
    token = None
    isvalid = False
    '''try:
        token = store.getToken(appID, user, api)
        # Validate the token
        isvalid = validator.isTokenValid(appID, user, token)
    except FileNotFoundError as error:
        print("No token was found for the appID and user combo. SO will try to fetch it from the authorization server.")
    except RuntimeError as rError:
        print("Runtime error occurred while retrieving tokens from token store")
        raise'''

    if isvalid:
        response = preparePositiveResponse(appID, token)
        return response
    else:
        # Get token from keycloak
        token = keycloak.getToken(appID, api)
        isvalid = validator.isTokenValid(appID, token)
        if isvalid:
            response = preparePositiveResponse(appID, token)
            return response
        else:
            response = prepareNegativeResponse(appID,  token)
            return response
