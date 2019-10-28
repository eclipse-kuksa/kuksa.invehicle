# Copyright (c) 2019 Eclipse Kuksa project
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0
#
# SPDX-License-Identifier: EPL-2.0
#
# Contributors: Robert Bosch GmbH

import unittest
import keycloakconnector
import tokenStore


class TestKeycloakMethods(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_token(self):
        test_secret = 'c27a7296-586b-4116-95ec-caf06e6b9854'
        test_client = 'Kuksa-dashboard'
        auth_url = 'http://localhost:8080/auth/'
        realm = 'Kuksa'

        keyclkconn = keycloakconnector.Keycloakconnector(auth_url, realm, test_client, test_secret)
        token = keyclkconn.getToken("", "")
        tokenStore.storeToken("Kuksa-dashboard", "w3c-vss", token)

    def test_get_certs(self):
        test_secret = 'c27a7296-586b-4116-95ec-caf06e6b9854'
        test_client = 'Kuksa-dashboard'
        auth_url = 'http://localhost:8080/auth/'
        realm = 'Kuksa'

        keyclkconn = keycloakconnector.Keycloakconnector(auth_url, realm, test_client, test_secret)
        cert = keyclkconn.getJWTPublickey()
        print(cert)


if __name__ == '__main__':
    unittest.main()
