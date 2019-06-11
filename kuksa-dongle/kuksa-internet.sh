#!/bin/bash

PROVIDER="vodafone.de"
NAME="vodafone"
PASSWORD="vodafone"

sleep 20s

cd /usr/lib/ofono/test

./enable-modem
sleep 1s
./create-internet-context vodafone.de vodafone vodafone
sleep 1s
./activate-context
sleep 1s
./online-modem

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
    cd /usr/lib/ofono/test

    ./enable-modem
     sleep 1s
    ./create-internet-context $PROVIDER $NAME $PASSWORD
     sleep 1s
    ./activate-context
     sleep 1s
    ./online-modem
  fi
sleep 10s
done
