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


def preparePositiveDaaResponse(appID, roles):
    resp = json.loads('{"appid": "", "roles" : ""}')
    resp["appid"] = appID
    resp["roles"] = roles
    return json.dumps(resp).encode("utf-8")  # Always return a valid JSON as string


def prepareNegativeDaaResponse(appID, roles):
    resp = json.loads('{"appid": "", "roles" : ""}')
    resp["appid"] = appID
    resp["roles"] = roles
    return json.dumps(resp).encode("utf-8")  # Always return a valid JSON as string


def processRequest(request):

    try:
        req_json = json.loads(request)

        # check if the request is coming from the direct-access-api client
        if req_json.get("daaid") is not None and req_json.get("daasecret") is not None:
            print('Direct-Access-API request received.')
            response = processDaaRequest(req_json)
            return response

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


def processDaaRequest(req_json):

    try:
        api = req_json["api"]
        appID = req_json["appid"]
        app_secret = req_json["secret"]

    except JSONDecodeError as error:
        print("Json decoding error occurred. The request is not in json format or does not contain the required fields")
        raise SyntaxError

    app_isvalid = False
    try:
        print('Retrieving client app token from the keycloak server = ' + auth_url)
        keycloak = keycloakconnector.Keycloakconnector(auth_url, realm, appID, app_secret)
        app_token = keycloak.getToken(appID, api)
        app_pubkey = keycloak.getJWTPublickey()
        audience = "account"
        app_isvalid = validator.isTokenValidAud(app_token, app_pubkey, audience)

        if app_isvalid:
            print('App token retrieved from keycloak server is valid')
            return retrieveClientRoles(req_json)

        else:
            print('App token retrieved from keycloak server is invalid')
            response = prepareNegativeDaaResponse(appID, app_token)
            return response
    except Exception as exp:
        print("An exception occurred while retrieving token {}".format(exp))
        response = prepareNegativeDaaResponse(appID, " ")
        return response


def retrieveClientRoles(req_json):
    try:
        api = req_json["api"]
        appID = req_json["appid"]
        daaID = req_json["daaid"]
        daa_secret = req_json["daasecret"]

    except JSONDecodeError as error:
        print("Json decoding error occurred. The request is not in json format or does not contain the required fields")
        raise SyntaxError

    try:
        print('Retrieving daa token from the keycloak server = ' + auth_url)
        keycloak = keycloakconnector.Keycloakconnector(auth_url, realm, daaID, daa_secret)
        daa_token = keycloak.getToken(daaID, api)
        daa_pubkey = keycloak.getJWTPublickey()
        audience = "account"
        daa_isvalid = validator.isTokenValidAud(daa_token, daa_pubkey, audience)

        if daa_isvalid:
            print('Daa token retrieved from keycloak server is valid, now retrieving client roles ')
            roles = keycloak.getClientRoles(appID, daa_token)
            response = preparePositiveDaaResponse(appID, roles)
            return response

        else:
            print('Daa token retrieved from keycloak server is invalid')
            response = prepareNegativeDaaResponse(daaID, daa_token)
            return response
    except Exception as exp:
        print("An exception occurred while retrieving token {}".format(exp))
        response = prepareNegativeDaaResponse(daaID, " ")
        return response
