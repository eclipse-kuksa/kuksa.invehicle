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
import unixsocket


class TestUnixSocketMethods(unittest.TestCase):

    def setUp(self):
        pass

    def test_create_server(self):
        unixsocket.createW3Csocket();


if __name__ == '__main__':
    unittest.main()
