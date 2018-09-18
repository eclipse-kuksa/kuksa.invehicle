#!/bin/bash

# Enter the MAC-ADDR of your bluetooth elm327 adapter here.
#MACID='00:11:03:01:04:35'
MACID='00:19:6D:36:7B:ED'
# Enter the pair key of your elm327 adapter here.
PAIRID='1234'

coproc bluetoothctl
echo -e "devices\n exit\n"  >&"${COPROC[1]}" 
devices=$(cat <&"${COPROC[0]}")
if [ `echo $devices | grep -c "$MACID"` -gt 0 ]
then
   echo "Device $MACID already paired"
   rfcomm unbind 0
   rfcomm bind 0 $MACID
else
   echo " Configure bluetooth connection with ELM Adapter "
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

echo " Configured $MACID with rfcomm0"

echo " Starting ELM 327 app"


SERIAL='/dev/rfcomm0'
TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJFeGFtcGxlIEpXVCIsImlzcyI6IkVjbGlwc2Uga3Vrc2EiLCJhZG1pbiI6dHJ1ZSwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE2MDkzNzI4MDB9.lxYf-N0C66NgJiinrY_pgVpZOxgH0ppnbMsdKfNiQjbMqYTY_nEpXufmjquvBaxiYsRb_3ScXA__gmviWj_PQoU3apuMVxJjAY6xrwaXFw7g-daUi21yqLSfLptH2vqQzhA_Y1LU6u7SjeiEcGRZrgq_bHnjMM61EVDSnKGCClo'


./elm327-visdatafeeder $SERIAL $TOKEN
