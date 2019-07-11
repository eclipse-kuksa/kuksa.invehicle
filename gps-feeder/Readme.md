# Traccar client

Simple KUKSA app that can send location data to the Traccar GPS tracking suite (https://www.traccar.org).

Does not use any KUKSA cloud service, instead it demonstrates how the platform can interact with existing cloud services

## Requirements
The client can access GPSD. For this it uses the gps3 library: https://pypi.org/project/gps3 or  https://github.com/wadda/gps3 
It uses python requests for talking to Traccar

Install it with 

`sudo pip3 install -r ./requirements.txt`


## Configuration file
The client triess to read traccar-client.ini in the current working directory, if that file is not found it tries /etc/traccar-client.ini

## Testing
How to get "real" GPS data easily on a PC.

Install gpsd on your Linux machine. If your distro starts it automatically stop it. In Ubuntu like this:

`sudo systemctl stop gpsd`
`sudo systemctl stop gpsd.socket`


Then start gpsd in Debug mode

`sudo gpsd -G  -n -N -D4 udp://*:3333`


Now GPSd awaits GPS data in NMEA format via UDP on port 3333. Many Android Apps can provide it, a totally free one is GPSDClient

https://play.google.com/store/apps/details?id=io.github.tiagoshibata.gpsdclient&rdid=io.github.tiagoshibata.gpsdclient

Start it, and let is stream to the ip of the computer you run GPSD on port 3333.

_Caveat_: It will only work if your phone has a _real_ GPS fix. (Just becasue Google maps shows some location guestimated form WiFi/cell towers is not enough)

## Test deplyoment
The start.sh script is suitable to be used for kuksa-hawkbit prototype in kuksa.invehicle

## Build install images
Small helper to build app packages suitable to be deployed with the prototype kuksa-downloader, in this folder execute

`./mktestpackage.sh`

Build SIMPLE_ and DOCKER_images. to save time (or if you have no docker installed) set `BUILD_DOCKER` to 0 in the script

### Kill and mark uninstalled
`pkill -ef  traccar-client.py`

If pkill is not available use grep and xargs.

`rm /tmp/gps_installed`
