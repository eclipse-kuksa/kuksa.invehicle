## Vehicle2Cloud app

This is an example kuksa-app which connects to the w3c-visserver service via Websocket and sends data to an Eclipse Hono instance. At the moment this sends the data to Hono's HTTP adapter.

## Running on AGL on Raspberry Pi 3

* Create an AGL image using the instructions in `agl-kuksa` project.
* Burn the image on to an SD card and boot the image on a Raspi 3.
* ssh into the raspi 3 with root.
* create self-signed cerificates using steps mentioned [here] (https://kb.op5.com/pages/viewpage.action?pageId=19073746#sthash.GHsaFkZe.dpbs) and rename the files to Client.key, Client.pem and CA.pem. Make sure you use the same CA while creating Server certificates.
* Then copy the Client.key, Client.pem and CA.pem to /usr/bin/vehicle2cloud using a ssh connection.
* Launch the app. Using command `./usr/bin/vehicle2cloud/vehicle2cloud 'HONO IP-ADDR' 'HONO-PORT' 'HONO-PASSWORD' 'HONO-DEVICE NAME'`


