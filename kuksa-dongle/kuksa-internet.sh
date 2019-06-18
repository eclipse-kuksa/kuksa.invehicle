#!/bin/bash

PROVIDER="web.vodafone.de"
NAME="vodafone"
PASSWORD="vodafone"

sleep 10s

# Temp fix to reset USB hub
echo 0 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio0/direction
echo 0 > /sys/class/gpio/gpio0/value
sleep 1s
echo 1 > /sys/class/gpio/gpio0/value

sleep 5s


cd /usr/lib/ofono/test
./enable-modem
if [[ "$?" != "0" ]];
    then
       echo "Some exception occured so need to restart ofono"
       systemctl restart ofono
fi

sleep 1s
./register-auto
sleep 1s
./create-internet-context $PROVIDER $NAME $PASSWORD
sleep 1s
./activate-context
sleep 3s
./process-context-settings
sleep 1s
./online-modem

sleep 30s

echo "Enabled modem with context. Now entering infinite loop for checking internet"

x=1
count=0
while [ $x -le 2 ]
do
   echo "Checking internet ..."
   if ping -q -c 1 -W 3 -w 3 8.8.8.8 >/dev/null; then
    echo "IPv4 is up"
  else
    echo "IPv4 is down so resetting context and re-enabling modem"
    cd /usr/lib/ofono/test
    ./enable-modem
    if [[ "$?" != "0" ]];
       then
         echo "Some exception occured so need to restart ofono"
         systemctl restart ofono
    fi
    sleep 1s
    ./deactivate-context
    sleep 1s
    ./register-auto
    sleep 1s
    ./create-internet-context $PROVIDER $NAME $PASSWORD
    sleep 1s
    ./activate-context
    sleep 3s
    ./process-context-settings
    sleep 1s
    ./online-modem
    count=$((count + 1))
    echo $count
  fi

sleep 15s
done
