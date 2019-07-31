#!/bin/bash

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

UPGRADE_AVAILABLE=`fw_printenv upgrade_available`

if [[ $UPGRADE_AVAILABLE = *1 ]]
then
	# Before we confirm the success of the upgrade, we can run an optional self check.
	# If the selfcheck command exists, run it and if it fails reboot the system to trigger a rollback.

	SELFCHECK=/usr/bin/kuksa-selfcheck

	if (command -v $SELFCHECK >/dev/null) && ! $SELFCHECK; then
		echo "Self check failed! Rebooting"
		reboot
		exit
	fi

	echo "System upgrade was successful. Setting upgrade_available to 0"

	# Make sure no rollback is triggered at next reboot.
	fw_setenv bootcount 0
	fw_setenv upgrade_available 0
fi
