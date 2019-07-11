#!/bin/bash
#
# Copyright (c) 2018 Eclipse KUKSA project
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0
#
# SPDX-License-Identifier: EPL-2.0
#
# Just a test for the prototype deployement, to be replaced later

echo "Marking Tracar GPS tracker  client installed"
touch /tmp/gps_installed

echo "Starting client"
python3 ./traccar-client.py
