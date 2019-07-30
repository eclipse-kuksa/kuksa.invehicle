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

import re
import subprocess


def get_boot_partition():
    result = subprocess.run(['fw_printenv', 'kuksa_root'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8').split('=')
    if len(output) == 2:
        return int(output[1])
    else:
        raise Exception("Could not get active boot partition")

def set_boot_partition(partition):
    subprocess.run(['fw_setenv', 'kuksa_root', str(partition)])
    subprocess.run(['fw_setenv', 'upgrade_available', '1'])


