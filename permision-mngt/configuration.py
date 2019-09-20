# Copyright (c) 2019 Eclipse Kuksa project
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0
#
# SPDX-License-Identifier: EPL-2.0
#
# Contributors: Robert Bosch GmbH
# This file handles the unix socket connection.

from configparser import SafeConfigParser


class PermConfig(object):

    def __init__(self, filename):
        parser = SafeConfigParser()
        parser.read(filename)

        self.__config__ = {}
        for section in parser.sections():
            temp = {}
            temp.update(parser.items(section))
            self.__dict__.__setitem__(section, temp)


configData = PermConfig('perm_manager.ini')


def getProperty(section, key):
    section = configData.__getattribute__(section)
    if section is None:
        return ' '
    else:
        return section[key]
