#!/bin/sh
#
# Copyright (c) 2018 Robert Bosch GmbH and others.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0
#
# SPDX-License-Identifier: EPL-2.0
# Forever checker for people so poor that they do not even have cron
#
# Contributors: Robert Bosch GmbH

# Enter the MAC-ADDR of your bluetooth elm327 adapter here.
MACID='00:11:03:01:04:35'
#MACID='00:19:6D:36:7B:ED'
# Enter the pair key of your elm327 adapter here.
PAIRID='6789'

coproc bluetoothctl
echo -e "devices\n exit\n"  >&"${COPROC[1]}" 
devices=$(cat <&"${COPROC[0]}")
if [ `echo $devices | grep -c "$MACID"` -gt 0 ]
then
   echo "Device $MACID already paired"
   rfcomm unbind 0
   rfcomm bind 0 $MACID
else
   echo "Configure new bluetooth connection with ELM Adapter "
   coproc bluetoothctl
   echo -e "agent on\n scan on\n"  >&"${COPROC[1]}" 
   sleep 25s  
   echo -e "pair $MACID\n"  >&"${COPROC[1]}"
   sleep 20s
   echo -e "$PAIRID\n exit\n"  >&"${COPROC[1]}"
   output=$(cat <&"${COPROC[0]}")
   echo $output
   sleep 5s
   rfcomm unbind 0
   rfcomm bind 0 $MACID
fi

echo "Configured $MACID with rfcomm0"
