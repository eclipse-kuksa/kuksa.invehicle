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

SUMMARY = "Network IDS initial contribution"
DESCRIPTION = "Network IDS for in-vehicle"
HOMEPAGE = ""
LICENSE = "EPL-2.0"
LIC_FILES_CHKSUM = "file://LICENSE;md5=c7cc8aa73fb5717f8291fcec5ce9ed6c"

inherit pkgconfig systemd
SRCREV = "${AUTOREV}"

SRC_URI = "git://github.com/eclipse/kuksa.invehicle.git;protocol=https" 
SRC_URI[sha256sum] = "0bf53c8f9c7306ec3dbc6c4c84335ca7ca758f04f93ec3bbd8e05292b3cc4344"

S = "${WORKDIR}/git/netIDS"

do_install_append(){
 install -d ${D]$(bindir}/netIDS
 install -m 0644 ${S}/TimeIntervals.py ${D]$(bindir}/netIDS
 install -d ${D}${systemd_system_unitdir}
 install -m 0644 ${S}/netIDS.service ${D}${systemd_system_unitdir}
 }
 
 SYSTEMD_SERVICE_${PN} = "netIDS.service"
