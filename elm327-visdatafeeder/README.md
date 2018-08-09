# ELM 327 OBD II Data Feeder for w3c-visserver

This is a simple data feeder to w3c-visserver service that reads OBD II data form a ELM 327 Bluetooth/USB dongle and pushes the data into the w3c-vis tree. At the moment reads very limited number of OBDII ( mode 1) values.

## Running on AGL on Raspberry Pi 3

* Create an AGL image using the instructions in `agl-kuksa` project.
* Burn the image on to an SD card and boot the image on a Raspi 3.
* ssh into the raspi 3 with root.
* create self-signed cerificates using steps mentioned [here](https://kb.op5.com/pages/viewpage.action?pageId=19073746#sthash.GHsaFkZe.dpbs) and rename the files to Client.key, Client.pem and CA.pem. Make sure you use the same CA while creating Server certificates.
* Then copy the Client.key, Client.pem and CA.pem to /usr/bin/elm327-visdatafeeder using a ssh connection.
* Launch the app. Using command `./usr/bin/elm327-visdatafeeder/elm327-visdatafeeder 'ELM-PORT'`
