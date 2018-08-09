## Vehicle2Cloud app

This is an example kuksa-app which connects to the w3c-visserver service via Websocket and sends data to an Eclipse Hono instance. At the moment this sends the data to Hono's HTTP adapter.

## Running on AGL on Raspberry Pi 3

* Create an AGL image using the instructions in `agl-kuksa` project.
* Burn the image on to an SD card and boot the image on a Raspi 3.
* ssh into the raspi 3 with root.
* Copy the vss data files https://github.com/GENIVI/vehicle_signal_specification/blob/master/vss_rel_1.0.csv and https://github.com/GENIVI/vehicle_signal_specification/blob/master/vss_rel_1.0.json into /usr/bin/
* Launch the app. Using command `./vehicle2cloud 'HONO IP-ADDR' 'HONO-PORT' 'HONO-PASSWORD' 'HONO-DEVICE NAME'`


