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

SUMMARY = "Wifi config for AGL-Kuksa"
DESCRIPTION = "Configures the default wifi to connect on boot"
HOMEPAGE = "https://www.eclipse.org/kuksa/"
LICENSE = "EPL-2.0"
LIC_FILES_CHKSUM = "file://LICENSE;md5=c7cc8aa73fb5717f8291fcec5ce9ed6c"

SRC_URI = "file://wifi_default.config \
           file://settings \
           file://LICENSE"

S = "${WORKDIR}"


do_install_append() {
  install -d ${D}${localstatedir}/lib/connman
  install -m 0644 ${S}/wifi_default.config ${D}${localstatedir}/lib/connman

  install -d ${D}${localstatedir}/lib/connman
  install -m 0644 ${S}/settings ${D}${localstatedir}/lib/connman
}
