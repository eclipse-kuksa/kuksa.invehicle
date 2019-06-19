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

SUMMARY = "Kuksa FOTA update Raspberry Pi"
DESCRIPTION = "Provides scripts for firmware over the air (FOTA) updates for the Raspberry Pi"
HOMEPAGE = "https://www.eclipse.org/kuksa/"
LICENSE = "EPL-2.0"
LIC_FILES_CHKSUM = "file://LICENSE;md5=c7cc8aa73fb5717f8291fcec5ce9ed6c"

RDEPENDS_${PN} = "\
		  python3 \
		  bash"

SRCREV = "${AUTOREV}"

SRC_URI = "\
	   git://github.com/eclipse/kuksa.invehicle.git;protocol=https \
	   file://kuksa-firmware-get-version \
	   file://kuksa-firmware-flash"

S = "${WORKDIR}/git/fota-raspberrypi"

FILES_${PN} += "${bindir}/kuksa/*"

do_install() {
  install -d ${D}${bindir}/kuksa
  install -m 0644 ${S}/kuksa/__init__.py ${D}${bindir}/kuksa

  install -d ${D}${bindir}/kuksa/firmware
  install -m 0644 ${S}/kuksa/firmware/__init__.py ${D}${bindir}/kuksa/firmware

  install -d ${D}${bindir}/kuksa/firmware/get-version
  install -m 0644 ${S}/kuksa/firmware/get-version/* ${D}${bindir}/kuksa/firmware/get-version

  install -d ${D}${bindir}/kuksa/firmware/flash
  install -m 0644 ${S}/kuksa/firmware/flash/* ${D}${bindir}/kuksa/firmware/flash

  install -d ${D}${bindir}
  install -m 0755 ${WORKDIR}/kuksa-firmware-get-version ${D}${bindir}/kuksa-firmware-get-version
  install -m 0755 ${WORKDIR}/kuksa-firmware-flash ${D}${bindir}/kuksa-firmware-flash
}
