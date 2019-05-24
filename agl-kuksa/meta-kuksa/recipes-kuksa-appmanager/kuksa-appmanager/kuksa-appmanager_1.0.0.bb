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

SUMMARY = "Kuksa AppManager"
DESCRIPTION = "Kuksa AppManager uses HawkBit artifacts to launch apps as Docker containers and initiate firmware updates"
HOMEPAGE = "https://www.eclipse.org/kuksa/"
LICENSE = "EPL-2.0"
LIC_FILES_CHKSUM = "file://LICENSE;md5=d9fc0efef5228704e7f5b37f27192723"

inherit systemd

RDEPENDS_${PN} = "\
          docker \
          python3 \
          python3-docker \
          python3-requests \
          python3-paho-mqtt \
          python3-typing"

SRCREV = "${AUTOREV}"

SRC_URI = "\
	   git://github.com/eclipse/kuksa.invehicle.git;protocol=https \
	   file://kuksa-appmanager.conf \
	   file://kuksa-appmanager.service"

S = "${WORKDIR}/git"

do_install() {
  install -d ${D}${bindir}/kuksa
  install -m 0644 ${S}/kuksa-appmanager/kuksa/__init__.py ${D}${bindir}/kuksa

  install -d ${D}${bindir}/kuksa/appmanager
  install -m 0644 ${S}/kuksa-appmanager/kuksa/appmanager/*.py ${D}${bindir}/kuksa/appmanager

  install -d ${D}${systemd_system_unitdir}
  install -m 0644 ${WORKDIR}/kuksa-appmanager.service ${D}${systemd_system_unitdir}

  install -d ${D}${sysconfdir}
  install -m 0644 ${WORKDIR}/kuksa-appmanager.conf ${D}${sysconfdir}
}

SYSTEMD_SERVICE_${PN} = "kuksa-appmanager.service"
