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
import OpenSSL
from OpenSSL.crypto import FILETYPE_PEM
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
