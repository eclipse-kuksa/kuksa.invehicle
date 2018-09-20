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

SUMMARY = "Kuksa hwakbit dowloader"
DESCRIPTION = "Downloader to facilitate download and installation of new kuksa apps"
HOMEPAGE = "https://www.eclipse.org/kuksa/"
LICENSE = "EPL-2.0"
LIC_FILES_CHKSUM = "file://LICENSE;md5=d9fc0efef5228704e7f5b37f27192723"  

SRCREV = "${AUTOREV}"

DEPENDS = "python3"

SRC_URI = "git://github.com/eclipse/kuksa.invehicle.git;protocol=https"
SRC_URI[sha256sum] = "0bf53c8f9c7306ec3dbc6c4c84335ca7ca758f04f93ec3bbd8e05292b3cc4344"
EXTRA_OECMAKE += "-Dpkg_config_libdir=${libdir} -DCMAKE_BUILD_TYPE=Release"

S = "${WORKDIR}/git/kuksa-hawkbit"

do_install_append() {
  install -d ${D}${bindir}/kuksa-hawkbit
  install -m 0644 ${S}/*.py ${D}${bindir}/kuksa-hawkbit
  install -d ${D}${bindir}/kuksa-hawkbit
  install -m 0644 ${S}/config.ini ${D}${bindir}/kuksa-hawkbit
  install -d ${D}${bindir}/kuksa-hawkbit/tools
  install -m 0755 ${S}/tools/foreverChecker.sh ${D}${bindir}/kuksa-hawkbit/tools
}




