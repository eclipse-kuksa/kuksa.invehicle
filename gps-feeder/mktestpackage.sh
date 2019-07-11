#!/bin/bash

# Copyright (c) 2018 Eclipse KUKSA project
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0
#
# SPDX-License-Identifier: EPL-2.0

BUILD_SIMPLE=1
BUILD_DOCKER=1


SIMPLE_TARGET=/tmp/SIMPLE_traccar.tar.bz2
DOCKER_TARGET=/tmp/DOCKER_traccar.tar.bz2


function build_simple {
    echo "Making SIMPLE_ package for Hawkbit"
	tar cvjf "$SIMPLE_TARGET" .

	echo "Package saved to $SIMPLE_TARGET"
	ls -ahl "$SIMPLE_TARGET"
}

function build_docker {
	echo "Making DOCKER_ package for Hawkbit"
	sudo docker build -t trac_packaging .
	sudo docker save trac_packaging | bzip2 -9 > "$DOCKER_TARGET"
	echo "Package saved to $DOCKER_TARGET"
	ls -ahl "$DOCKER_TARGET"
}


if [ $BUILD_SIMPLE -eq 1 ]
then
  echo "Making simple package"
  build_simple
fi



if [ $BUILD_DOCKER -eq 1 ]
then
	echo "Making Docker export"
	build_docker
fi



