# Kuksa OBD dongle

Kuksa OBD Dongle is hardware platform for based on Raspberry pi Compute Module 3, which illustrates kuksa functionalities for an Aftermarket or Retrofit Solution.

The Dongle has the following features

* OBDII Connector.
* LTE Module (Sierra Wireless EM7455) with SIM card holder.
* 2 USB 2.0 Ports.
* Raspberry Pi CM3 (with or without integrated flash memory).
* mini HDMi port.
* Voltage converter from 12V.

![Alt text](./logos/kuksa_dongle.png?raw=true "Eclipse kuksa dongle")

The kuksa dongle connects to the OBD port in the car and draws power from the OBD port. It can run any flavour of Linux on the CM3 and would enable the LTE Module for Internet connection.
It can basically read OBD II related data from the car and establish connection to the cloud through the LTE connection and provides a platform for deploying kuksa invehicle software components.

## Build and run AGL-Kuksa for kuksa-obd-dongle

If you are building agl-kuksa from first principles using the instructions from the AGL getting started website, you just need to make sure the KERNEL_IMAGETYPE variable in build/conf/local.conf to "zImage" like this

KERNEL_IMAGETYPE="zImage"

This should do the trick.


If you are using the Cmake wrapper to build AGL, follow the steps below.

* go to `kuksa.invehicle/agl-kuksa` and create a new directory named build and go to build dir. use `mkdir build ; cd build`
* now execute `cmake ..`
* Once the above command is executed, go to `meta-agl-bsp/conf/include` and open file `agl_raspberrypi3.inc` in the file change value of key `KERNEL_IMAGETYPE` to `zImage`.
* Now go back to the `kuksa.invehicle/agl-kuksa/build` dir and execute `make agl-kuksa`.

This will take sometime to finish, once it is done the kuksa-dongle image should be ready.


* Once the image is built, make sure you change the cmdline.txt file in the boot partion nad remove the console0 entry there. Because this UART is used by the OBD II port internally.
* Add the dtparam in the config.txt fould in gpio.txt file.
* You may also need to manually copy the script to enable the modem and also the associated service file. 

 
