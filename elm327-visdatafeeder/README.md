# ELM 327 OBD II Data Feeder for w3c-visserver

This is a simple data feeder to w3c-visserver service that reads OBD II data form a ELM 327 Bluetooth/USB dongle and pushes the data into the w3c-vis tree. At the moment reads very limited number of OBDII ( mode 1) values.

# Builing with CMake
* Go to the folder elm327-visdatafeeder and create a new directory build using `mkdir build`
* Change directory using `cd build`
* Execure cmake using `cmake ..`
* Build using the command `make`
* Execute using command `.start.sh`. This will start the app using demo certificates and JWT Token found in the example/demo-certificates folder.

## Running on AGL on Raspberry Pi 3

* Create an AGL image using the instructions in `agl-kuksa` project.
* Burn the image on to an SD card and boot the image on a Raspi 3.
* elm327-visdatafeeder is deployed as a systemd service `elm327-visdatafeeder.service` which connects to w3c-visserver on port 8090.


## Creating own certificates and JWT Tokens
Refer to the readme in w3c-visserver-api under how to section.
