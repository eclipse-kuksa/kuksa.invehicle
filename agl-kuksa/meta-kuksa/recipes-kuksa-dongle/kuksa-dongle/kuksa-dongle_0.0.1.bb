# ******************************************************************************
# Copyright (c) 2019 Robert Bosch GmbH and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# https://www.eclipse.org/org/documents/epl-2.0/index.php
#
#  Contributors:
#      Robert Bosch GmbH - kuksa dongle API and functionality
# *****************************************************************************

SUMMARY = "kuksa dongle related services"
DESCRIPTION = "Services to enable LTE, GPS and Standby mode in kuksa-dongle"
HOMEPAGE = "https://www.eclipse.org/kuksa/"
LICENSE = "EPL-2.0"
LIC_FILES_CHKSUM = "file://LICENSE;md5=d9fc0efef5228704e7f5b37f27192723"

inherit systemd pkgconfig

SRCREV = "${AUTOREV}"

RDEPENDS_${PN} += " bash python3-core"

SRC_URI = "git://github.com/eclipse/kuksa.invehicle.git;protocol=https;branch=kuksa-obd-dongle-components"
SRC_URI[sha256sum] = "0bf53c8f9c7306ec3dbc6c4c84335ca7ca758f04f93ec3bbd8e05292b3cc4344"
EXTRA_OECMAKE += "-Dpkg_config_libdir=${libdir} -DCMAKE_BUILD_TYPE=Release"

S = "${WORKDIR}/git/kuksa-dongle"

do_install_append() {
  install -d ${D}${bindir}/kuksa-dongle
  install -m 0755 ${S}/kuksa-standby.sh ${D}${bindir}/kuksa-dongle
  install -d ${D}${bindir}/kuksa-dongle
  install -m 0755 ${S}/ofono-fix.py ${D}${bindir}/kuksa-dongle
  install -d ${D}${bindir}/kuksa-dongle
  install -m 0755 ${S}/internet-status.py ${D}${bindir}/kuksa-dongle
  install -d ${D}${systemd_system_unitdir}
  install -m 0644 ${S}/systemd/kuksa-ofono-fix.service ${D}${systemd_system_unitdir}
  install -d ${D}${systemd_system_unitdir}
  install -m 0644 ${S}/systemd/kuksa-standby.service ${D}${systemd_system_unitdir}
  install -d ${D}${systemd_system_unitdir}
  install -m 0644 ${S}/systemd/kuksa-internet-status.service ${D}${systemd_system_unitdir}
}

SYSTEMD_SERVICE_${PN} = " kuksa-ofono-fix.service kuksa-standby.service kuksa-internet-status.service"
