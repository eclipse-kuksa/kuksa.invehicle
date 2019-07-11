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

SUMMARY = "ELM 327 VIS Data feeder"
DESCRIPTION = "OBD II data feeder for W3C VIS Server"
HOMEPAGE = "https://www.w3.org/TR/vehicle-information-api/"
LICENSE = "EPL-2.0"
LIC_FILES_CHKSUM = "file://LICENSE;md5=d9fc0efef5228704e7f5b37f27192723"

inherit pkgconfig cmake systemd
SRCREV = "${AUTOREV}"

DEPENDS = "boost openssl"
RDEPENDS_${PN} += "bash"

SRC_URI = "git://github.com/rai20/kuksa.invehicle.git;protocol=https;branch=kuksa-dongle"
SRC_URI_append = " file://bt_setup.sh "
SRC_URI[sha256sum] = "0bf53c8f9c7306ec3dbc6c4c84335ca7ca758f04f93ec3bbd8e05292b3cc4344"
EXTRA_OECMAKE += "-Dpkg_config_libdir=${libdir} -DCMAKE_BUILD_TYPE=Release"

S = "${WORKDIR}/git/elm327-visdatafeeder"

do_install_append() {
  install -d ${D}${systemd_system_unitdir}
  install -m 0644 ${S}/systemd/elm327-visdatafeeder.service ${D}${systemd_system_unitdir}

  install -d ${D}${bindir}/elm327-visdatafeeder
  install -m 0755 ${WORKDIR}/bt_setup.sh ${D}${bindir}/elm327-visdatafeeder
}

SYSTEMD_SERVICE_${PN} = "elm327-visdatafeeder.service"
