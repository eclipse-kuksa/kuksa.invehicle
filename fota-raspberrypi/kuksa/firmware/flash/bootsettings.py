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

def get_boot_partition(cmdline_path):
    with open(cmdline_path, "r") as f:
        line = f.read()

        # We expect the cmdline.txt file to have exactly one line that contains a segment like this:
        # ... root=PARTUUID=b598b92e-03 ... where 3 is indicating the current boot partition
        return int(re.search("root=.*?(.) ", line).group(1))


def set_boot_partition(cmdline_path, partition):
    with open(cmdline_path, "r") as f:
        line = f.read()

    # Replace partition number with new partition
    line = re.sub("(root=.*?)(.) ", r"\g<1>" + str(partition) + " ", line)

    # Save file
    with open(cmdline_path, "w") as f:
        f.write(line)

