SUMMARY = "A Python library for the Docker Engine API."
HOMEPAGE = "https://github.com/docker/docker-py"
LICENSE = "Apache-2.0"
LIC_FILES_CHKSUM = "file://LICENSE;md5=34f3846f940453127309b920eeb89660"

inherit pypi setuptools3

SRC_URI[md5sum] = "eff98d9a2e76a6b093def63787e49b49"
SRC_URI[sha256sum] = "e3815a4f55f6ac78cb3fa4afbc17e923d7bfd08a3da0ceecd313a6dfa3fa4a97"

DEPENDS += "${PYTHON_PN}-pip-native"

RDEPENDS_${PN} += " \
	python3-docker-pycreds \
	python3-requests \
	python3-websocket-client \
"

