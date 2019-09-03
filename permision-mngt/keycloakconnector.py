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


from keycloak import KeycloakOpenID


class Keycloakconnector:
    keycloak_openid = None

    def __init__(self, serverurl, realm, clientid, secret):
        self.keycloak_openid = KeycloakOpenID(server_url=serverurl,
                                              client_id=clientid,
                                              realm_name=realm,
                                              client_secret_key=secret,
                                              verify=True)
        config_well_know = self.keycloak_openid.well_know()
        #print(config_well_know)

    def getToken(self, appID, api):
        token = self.keycloak_openid.token(username="", password="", grant_type=["client_credentials"])
        token = token['access_token']
        print("Access token = ")
        print(token)
        return token

    # Get JWT public key.
    def getJWTPublickey(self, url):
        return ""
