# *****************************************************************************
#  Copyright (c) 2018 Fraunhofer IEM and others
#
#  This program and the accompanying materials are made available under the
#  terms of the Eclipse Public License 2.0 which is available at
#  http://www.eclipse.org/legal/epl-2.0
#
#  SPDX-License-Identifier: EPL-2.0
#
#  Contributors: Fraunhofer IEM
# *****************************************************************************

SUMMARY = "App IDS"
DESCRIPTION = "Implementation of the STIDE Intrusion Detection Approach"
HOMEPAGE = ""
LICENSE = "EPL-2.0"
LIC_FILES_CHKSUM = "file://LICENSE;md5=c7cc8aa73fb5717f8291fcec5ce9ed6c"

inherit systemd

#Add a release revision as soon as this is stable
SRCREV = "${AUTOREV}"

RDEPENDS_${PN} = "\
		  python3 \
		  python3-lxml \
		  python3-paho-mqtt \
		  python3-psutil \
		  sqlite \
		  mosquitto \
		  strace"

SRC_URI = "\
	   git://github.com/eclipse/kuksa.invehicle.git;protocol=https;\
	   file://syscall_tracer.service \
	   file://stide_syscall_formatter.service \
	   file://stide.service"
 
SRC_URI[sha256sum] = "dd91a39785fba3129517c44522145afc00a89bce5e2e10f49893637a8e817a29"

#Forces an automatic update whenever the revision of the source code changes.
#Remove this for release builds.
PV = "0.0.1+git${SRCPV}"

S = "${WORKDIR}/git/app-ids"

do_install () {
  install -d ${D}${bindir}/app-ids

  install -d ${D}${bindir}/app-ids/src
  install -m 0644 ${S}/src/syscall_tracer.py ${D}${bindir}/app-ids/src
  install -m 0644 ${S}/src/stide_syscall_formatter.py ${D}${bindir}/app-ids/src
  install -m 0644 ${S}/src/stide.py ${D}${bindir}/app-ids/src
  install -m 0644 ${S}/src/config.xml ${D}${bindir}/app-ids/src

  install -d ${D}${bindir}/app-ids/src/xml_validation
  install -m 0644 ${S}/src/xml_validation/configuration_file.xsd ${D}${bindir}/app-ids/src/xml_validation/configuration_file.xsd
  install -m 0644 ${S}/src/xml_validation/stide_syscall_formatter_xml.xsd ${D}${bindir}/app-ids/src/xml_validation/stide_syscall_formatter_xml.xsd
  install -m 0644 ${S}/src/xml_validation/syscall_tracer_xml.xsd ${D}${bindir}/app-ids/src/xml_validation/syscall_tracer_xml.xsd

  install -d ${D}${systemd_system_unitdir}
  install -m 0644 ${WORKDIR}/syscall_tracer.service ${D}${systemd_system_unitdir}
  install -m 0644 ${WORKDIR}/stide_syscall_formatter.service ${D}${systemd_system_unitdir}
  install -m 0644 ${WORKDIR}/stide.service ${D}${systemd_system_unitdir}
}

SYSTEMD_SERVICE_${PN} = "\
			syscall_tracer.service \
			stide_syscall_formatter.service \
			stide.service "

SYSTEMD_AUTO_ENABLE_${PN} = "disable"
