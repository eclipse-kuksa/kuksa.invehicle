# Copyright (c) 2019 Eclipse Kuksa project
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0
#
# SPDX-License-Identifier: EPL-2.0
#
# Contributors: Robert Bosch GmbH

# This file takes care of the communication with keycloak for retrieving the Tokens.
from json import JSONDecodeError

import OpenSSL
from OpenSSL.crypto import FILETYPE_PEM
from keycloak import KeycloakOpenID
from requests import get
import json


class Keycloakconnector:
    keycloak_openid = None

    def __init__(self, serverurl, realm, clientid, secret):
        self.keycloak_openid = KeycloakOpenID(server_url=serverurl,
                                              client_id=clientid,
                                              realm_name=realm,
                                              client_secret_key=secret,
                                              verify=True)
        config_well_know = self.keycloak_openid.well_know()
        self.serverurl = serverurl
        self.realm = realm
        # print(config_well_know)

    def getToken(self, appID, api):
        token = self.keycloak_openid.token(username="", password="", grant_type=["client_credentials"])
        token = token['access_token']
        print("Access token = ")
        print(token)
        return token

    # Get JWT public key.
    def getJWTPublickey(self):
        cert = self.keycloak_openid.certs()
        if cert is None:
            return ""
        x5c = cert.get('keys')[0]['x5c'][0]
        x5c = '-----BEGIN CERTIFICATE-----\n' + x5c + '\n-----END CERTIFICATE-----'
        x509 = OpenSSL.crypto.load_certificate(FILETYPE_PEM, x5c)
        pubkey = x509.get_pubkey()
        pubkey = OpenSSL.crypto.dump_publickey(FILETYPE_PEM, pubkey).decode("utf-8")
        return pubkey

    def getClientRoles(self, clientid, daa_token):
        api_call_headers = {'Authorization': 'Bearer ' + daa_token, 'cache-control': "no-cache",
                            "Content-Type": "application/json", "charset": "utf-8"}

        roles = ""

        try:
            # get keycloak client representation (needed to get the value of id_of_client parameter)
            client_url = self.serverurl + "admin/realms/" + self.realm + "/clients?clientId=" + clientid
            client_rep = get(client_url, headers=api_call_headers)
            client_json = json.loads(client_rep.text)
            id_of_client = client_json[0]["id"]
            print(id_of_client)

            # get client roles
            roles_url = self.serverurl + "admin/realms/" + self.realm + "/clients/" + id_of_client + "/roles"
            roles_rep = get(roles_url, headers=api_call_headers)
            keycloak_roles = json.loads(roles_rep.text)

            if "can_id_read" in keycloak_roles[0]:
                can_id_read_array = keycloak_roles[0]["description"].split(",")
                can_id_write_array = keycloak_roles[1]["description"].split(",")
            else:
                can_id_read_array = keycloak_roles[1]["description"].split(",")
                can_id_write_array = keycloak_roles[0]["description"].split(",")

            roles = json.loads('{"can_id_read": "", "can_id_write" : ""}')
            roles["can_id_read"] = can_id_read_array
            roles["can_id_write"] = can_id_write_array

        except JSONDecodeError as error:
            print(
                "Json decoding error occurred. Input is not in json format or does not contain the required fields")
            raise SyntaxError
        except Exception as exp:
            print("An exception occurred while retrieving client roles {}".format(exp))

        return roles

