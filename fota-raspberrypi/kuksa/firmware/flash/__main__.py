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

import json
import lzma
import os
import sys
import shutil
import subprocess

from . import __version__
from . import bootsettings
from . import partitions

# Settings
partition1 = 2
partition2 = 3
partition_base_path = "/dev/mmcblk0p"
cmdline_path = "/boot/cmdline.txt"
boot_path = "/boot"

tmp_file = "/tmp/bootpartition"
mount_dir = "/tmp/mnt"

def extract_boot_partition(imgFile, partition):
    print("Extracting boot partition")
    # Extract boot partition to temporary file and mount it
    partitions.extract_partition(imgFile, partition, tmp_file)
    if (not os.path.isdir(mount_dir)):
        os.mkdir(mount_dir)
    subprocess.check_call(["mount", tmp_file, mount_dir])

    # Delete the contents of boot_path
    for f in os.listdir(boot_path):
        rm_path = os.path.join(boot_path, f)
        if (os.path.isdir(rm_path)):
            shutil.rmtree(rm_path)
        else:
            os.remove(rm_path)

    # Copy boot files to boot_path
    for f in os.listdir(mount_dir):
        copy_path = os.path.join(mount_dir, f)
        if (os.path.isdir(copy_path)):
            shutil.copytree(copy_path, os.path.join(boot_path, f))
        else:
            shutil.copy(copy_path, boot_path)

    # Unmount and remove temporary file and mount dir
    subprocess.check_call(["umount", mount_dir])
    os.remove(tmp_file)
    os.removedirs(mount_dir)


def extract_rootfs_partition(image_file, partition, partition_path):
    print("Extracting rootfs partition")
    partitions.extract_partition(image_file, partition, partition_path)


def flash_osimage(image_file, partition_path):
    partition_table = partitions.read_partition_table(image_file)
    if len(partition_table) < 2:
        raise Exception("Expecting at least 2 partitions in image (boot and rootfs). Found {}".format(len(partition_table)))
    # Extract rootfs first, if that fails for some reason, we don't want to overwrite the boot files
    extract_rootfs_partition(image_file, partition_table[1], partition_path)
    extract_boot_partition(image_file, partition_table[0])


def firmware_flash(files):
    # Find out which partition to flash
    current_partition = bootsettings.get_boot_partition(cmdline_path)
    new_partition = partition1 if current_partition == partition2 else partition2
    partition_path = "{}{}".format(partition_base_path, new_partition)

    # We need exactly one file. It can be either an uncompressed image (.img) or a LZMA compressed image (.xz)
    if (len(files) != 1):
        raise Exception("Expecting exactly one file to flash os image")

    f = files[0]

    if f["path"].lower().endswith(".img"):
        # Uncompressed image
        print("Opening uncompressed image file {}".format(f["path"]))
        with open(f["path"], "rb") as image_file:
            flash_osimage(image_file, partition_path)
    elif f["path"].lower().endswith(".xz"):
        # LZMA compressed image
        print("Opening compressed image file {}".format(f["path"]))
        with lzma.open(f["path"]) as image_file:
            flash_osimage(image_file, partition_path)
    else:
        raise Exception("Unsupported image file type (supported: .img and .xz)")

    print("Setting boot partition to {}".format(new_partition))
    bootsettings.set_boot_partition(cmdline_path, new_partition)
    print("Rebooting...")
    os.system("reboot")


if __name__ == "__main__":

    print("Kuksa firmware flasher version {}".format(__version__))

    print("Expecting one line of JSON config:")
    line = sys.stdin.readline()
    config = json.loads(line)

    print("Received JSON config:")
    print("Name: {}".format(config["name"]))
    print("Version: {}".format(config["version"]))

    firmware_flash(config["files"])

