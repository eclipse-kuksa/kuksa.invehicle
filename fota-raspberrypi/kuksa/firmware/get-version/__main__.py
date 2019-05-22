# Copyright (c) 2019 Eclipse KUKSA project
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0
#
# SPDX-License-Identifier: EPL-2.0
#
# Contributors:
#  Paderborn University

import sys
import re

def firmware_get_version(name):
    if (name == "osimage"):
        # Open /etc/os-release to check the installed firmware version
        with open("/etc/os-release") as f:
            for line in f:
                if ('=' not in line):
                    continue
                key, value = line.rstrip().split("=", 1)
                if (key == "VERSION_ID"):
                    # The value can be enclosed by single or double quotes
                    return value.strip('"').strip("'")
            raise Exception("Could not find VERSION_ID key in /etc/os-release file")
    else:
        raise Exception("Only supported firmware is osimage")


if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("Please add the firmware name as a parameter")
        exit(-1)

    print(firmware_get_version(sys.argv[1]))

