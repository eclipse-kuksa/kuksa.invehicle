#!/bin/bash

PROVIDER="web.vodafone.de"
NAME="vodafone"
PASSWORD="vodafone"

sleep 20s

cd /usr/lib/ofono/test

./enable-modem
sleep 1s
./online-modem
sleep 1s
./register-auto
sleep 1s
./create-internet-context $PROVIDER $NAME $PASSWORD
sleep 1s
./activate-context
sleep 5s
./process-context-settings

sleep 30s

echo "Enabled modem with context. Now entering infinite loop for checking internet"

x=1
while [ $x -le 2 ]
do
   echo "Checking internet ..."
   if ping -q -c 1 -W 1 -w 5 8.8.8.8 >/dev/null; then
    echo "IPv4 is up"
  else
    echo "IPv4 is down so resetting context and re-enabling modem"
    echo "Restarting ofono service"
    systemctl restart ofono
    sleep 5s
    cd /usr/lib/ofono/test
    ./enable-modem
    sleep 1s
    ./online-modem
    sleep 1s
    ./register-auto
    sleep 1s
    ./create-internet-context $PROVIDER $NAME $PASSWORD
    sleep 1s
    ./activate-context
    sleep 5s
    ./process-context-settings

  fi
sleep 15s
done

