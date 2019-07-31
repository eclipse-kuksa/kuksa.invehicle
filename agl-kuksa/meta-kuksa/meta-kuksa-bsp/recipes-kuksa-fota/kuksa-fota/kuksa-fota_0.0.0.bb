# ******************************************************************************
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
# *****************************************************************************

SUMMARY = "Dummy FOTA update"
DESCRIPTION = "Dummy FOTA scripts that exit with an error. Should be overlayed by platform specific FOTA scripts."
HOMEPAGE = "https://www.eclipse.org/kuksa/"
LICENSE = "EPL-2.0"
LIC_FILES_CHKSUM = "file://LICENSE;md5=c7cc8aa73fb5717f8291fcec5ce9ed6c"

RDEPENDS_${PN} = "bash"

SRC_URI = "file://kuksa-firmware-dummy \
           file://LICENSE"

S = "${WORKDIR}"

do_install() {
  install -d ${D}${bindir}
  install -m 0755 ${WORKDIR}/kuksa-firmware-dummy ${D}${bindir}/kuksa-firmware-get-version
  install -m 0755 ${WORKDIR}/kuksa-firmware-dummy ${D}${bindir}/kuksa-firmware-flash
}
