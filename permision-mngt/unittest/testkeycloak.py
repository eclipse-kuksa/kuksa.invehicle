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
        test_secret = '807cc5c6-da4b-43b7-a77f-d957145fc049'
        test_client = 'Kuksa-dashboard'
        auth_url = 'http://localhost:8080/auth/'
        realm = 'Kuksa'

        keyclkconn = keycloakconnector.Keycloakconnector(auth_url, realm, test_client, test_secret)
        token = keyclkconn.getToken("", "")
        tokenStore.storeToken("Kuksa-dashboard", "w3c-vss", token)


if __name__ == '__main__':
    unittest.main()
