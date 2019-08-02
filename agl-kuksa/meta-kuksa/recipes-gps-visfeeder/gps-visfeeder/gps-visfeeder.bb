# ******************************************************************************
# Copyright (c) 2018 Robert Bosch GmbH and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# https://www.eclipse.org/org/documents/epl-2.0/index.php
#
#  Contributors:
#      Robert Bosch GmbH - initial API and functionality
# *****************************************************************************

SUMMARY = "GPS data feeder for W3C VIS server"
DESCRIPTION = "Feeds GPS data into w3c visserver"
HOMEPAGE = "https://www.w3.org/TR/vehicle-information-api/"
LICENSE = "EPL-2.0"
LIC_FILES_CHKSUM = "file://LICENSE;md5=c7cc8aa73fb5717f8291fcec5ce9ed6c"

inherit pkgconfig systemd
SRCREV = "${AUTOREV}"

RDEPENDS_${PN} += " python3"

SRC_URI = "git://github.com/eclipse/kuksa.invehicle.git;protocol=https;branch=kuksa-obd-dongle-components"
SRC_URI[sha256sum] = "0bf53c8f9c7306ec3dbc6c4c84335ca7ca758f04f93ec3bbd8e05292b3cc4344"
EXTRA_OECMAKE += "-Dpkg_config_libdir=${libdir} -DCMAKE_BUILD_TYPE=Release"

S = "${WORKDIR}/git/gps-visfeeder"

do_install_append() {
  install -d ${D}${bindir}/gps-visfeeder
  install -m 0644 ${S}/*.py ${D}${bindir}/gps-visfeeder

  install -d ${D}${bindir}/gps-visfeeder
  install -m 0644 ${S}/*.ini ${D}${bindir}/gps-visfeeder

  install -d ${D}${bindir}/gps-visfeeder
  install -m 0644 ${S}/*.csv ${D}${bindir}/gps-visfeeder

  install -d ${D}${bindir}/gps-visfeeder
  install -m 0644 ${S}/*.txt ${D}${bindir}/gps-visfeeder

  install -d ${D}${bindir}/gps-visfeeder/providers
  install -m 0644 ${S}/providers/*.py ${D}${bindir}/gps-visfeeder/providers

  install -d ${D}${systemd_system_unitdir}
  install -m 0644 ${S}/systemd/gps-visfeeder.service ${D}${systemd_system_unitdir}
}

SYSTEMD_SERVICE_${PN} = "gps-visfeeder.service"
