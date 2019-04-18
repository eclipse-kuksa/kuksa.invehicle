# *****************************************************************************
#  Copyright (c) 2018 Fraunhofer IEM and others
#
#  This program and the accompanying materials are made available under the
#  terms of the Eclipse Public License 2.0 which is available at
#  http://www.eclipse.org/legal/epl-2.0
#
#  SPDX-License-Identifier: EPL-2.0
#
#  Contributors: Fraunhofer IEM - append group and userid for mosquitto
# *****************************************************************************

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI += "\
        file://mosquitto.conf \
"

USERADD_GID_TABLES += "recipes-connectivity/mosquitto/files/group"
USERADD_UID_TABLES += "recipes-connectivity/mosquitto/files/passwd"

do_install_append() {
  install -m 0644 ${WORKDIR}/mosquitto.conf ${D}${sysconfdir}/mosquitto
}

FILES_${PN} += "${sysconfdir}/mosquitto/mosquitto.conf"
