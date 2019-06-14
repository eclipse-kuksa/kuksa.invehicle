#!/bin/sh

echo 7 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio7/direction
echo 0 > /sys/class/gpio/gpio7/value

echo 9 > /sys/class/gpio/export
echo in > /sys/class/gpio/gpio9/direction

while true
do

res=$(cat /sys/class/gpio/gpio9/value)
if [ $res -eq 1 ]
then

halt

fi
sleep 1s

done

