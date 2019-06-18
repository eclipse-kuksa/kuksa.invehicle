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
echo "pin9 is high wait for 0.5 more seconds and if it is still high board will be shut down."
sleep 0.5s
res=$(cat /sys/class/gpio/gpio9/value)
if [ $res -eq 1 ] 
then
#echo "Waited 0.5 seconds and the pin9 is still high so shutting down"
#halt
# FIX this- At the moment pi is not shut down but simply the power is removed.
echo 1 > /sys/class/gpio/gpio7/value
fi
fi
sleep 2s

done

