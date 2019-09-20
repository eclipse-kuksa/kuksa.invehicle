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

import configuration


class TestConfMethods(unittest.TestCase):

    def test_getkey(self):
        val = configuration.getProperty('keycloak', 'realm')
        assert val == 'kuksa'


if __name__ == '__main__':
    unittest.main()
