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

import struct

def read_partition_table(fin):
    # Read the master boot record containing the partition table
    mbr = bytearray(512)
    fin.readinto(mbr)

    # MBR must end with boot signature 0x55 0xaa
    if (mbr[510] != 0x55 or mbr[511] != 0xaa):
        raise Exception("No master boot record found")

    # The partition table starts at byte 446 and is 64 bytes long
    bytes = mbr[446:510]
    partition_table = []
    # The partition table consists of up to 4 partition entries, 16 bytes each
    for i in range(4):
        partition_entry = read_partition_entry(bytes[i*16:(i+1)*16])
        if partition_entry is not None:
            partition_table.append(partition_entry)
    return partition_table


def read_partition_entry(bytes):
    boot_flag = bytes[0]
    partition_type = bytes[4]
    sectors = struct.unpack("<II", bytes[8:16])

    if partition_type == 0: return None

    partition_entry = {}
    partition_entry["bootable"] = boot_flag == 0x80
    partition_entry["type"] = partition_type
    partition_entry["startsector"] = sectors[0]
    partition_entry["sectors"] = sectors[1]
    return partition_entry


def extract_partition(fin, partition_entry, path, sector_size = 512):
    startsector = partition_entry["startsector"]
    sectors = partition_entry["sectors"]

    # Jump to start of partition
    fin.seek(startsector * sector_size)

    progress = 0
    with open(path, "wb") as fout:
        for i in range(sectors):
            bytes = fin.read(sector_size)
            fout.write(bytes)
            progress += sector_size

