# ******************************************************************************
# Copyright (c) 2018 SecurityMatters.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# https://www.eclipse.org/org/documents/epl-2.0/index.php
#
#  Contributors:
#      Robert Bosch GmbH - initial API and functionality
#      SecurityMatters - network IDS first version
# *****************************************************************************

SUMMARY = "ELM 327 VIS Data feeder"
DESCRIPTION = "Network IDS for in-vehicle"
HOMEPAGE = ""
LICENSE = "EPL-2.0"
LIC_FILES_CHKSUM = ""

inherit pkgconfig cmake
SRCREV = "${AUTOREV}"

 DEPENDS = "python3-native, python-numpy"

SRC_URI = "git://github.com/eclipse/kuksa.invehicle.git;protocol=https" 
SRC_URI[sha256sum] = ""
BBCLASSEXTEND = "native"

BUILDARGS = "5 vcan0 true"

S = "${WORKDIR}/git/netIDS"
