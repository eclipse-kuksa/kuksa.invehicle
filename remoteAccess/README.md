## Remote Access app

This is an example kuksa-app which connects to the w3c-visserver service via Websocket and talks to the Eclipse Hono MQTT adapter. Using this app commands can be sent to the vehicle remotely.
This app requires  minimum Hono 0.7 version.

## Builing with CMake
* Go to the folder remoteaccess and create a new directory build using `mkdir build`
* Change directory using `cd build`
* Execure cmake using `cmake ..`
* Build using the command `make`
* Execute using command `.start.sh`. This will start the app using demo certificates and JWT Token found in the example/demo-certificates folder.  

## Running on AGL on Raspberry Pi 3

* Create an AGL image using the instructions in `agl-kuksa` project.
* Burn the image on to an SD card and boot the image on a Raspi 3.
* ssh into the raspi 3 with root.
* Go to directory `/usr/bin/remoteaccess`.
* Launch the app. Using command `./start.sh`

## Creating own certificates and JWT Tokens
Refer to the readme in w3c-visserver-api under how to section.

