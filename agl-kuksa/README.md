# AGL KUKSA Build and Run on Raspberry PI 3

Kuksa is a wrapper project around Automotive Grade Linux (AGL). From its side,
AGL uses Yocto/Bitbake building system to build an automotive domain specific
Linux distribution. Therefore, this projects provides a building system that
adds Kuksa's specific Bitbake layers on top of the original AGL. The scripts in 
this project help ease the process of building an AGL image by simple using a few
commands. This project includes the yocto recipes found in meta-kuksa project.


# Dependencies

To be able to build this AGL image first install the building dependencies by
running;

```
  apt install cmake curl chrpath build-essential texinfo
```

# Build the Image/SDK with cmake scripts


## Prerequisites:

1. Need Ubuntu 16

2. Fast Internet connection.

3. Minimum of 100 GB memory.

4. Some patience as it takes about 8 hours the first time.


To build the Image/SDK, run;

```
  cd <agl-kuksa-root>
  mkdir build
  cd build
  cmake ..
  make <agl-kuksa-target>
```

Where `<agl-kuksa-target>` can be;

* `agl-kuksa`: AGL kuksa image and SDK
*  Other Targets to follow.

The output images can be seen at `<agl-kuksa-root>/build/images` and the SDKs at `<agl-kuksa-root>/build/sdk`.

# Build the Image using yocto/bitbake

## Prerequisites


1. Need Ubuntu 16

2. Fast Internet connection.

3. Minimum of 100 GB memory.

4. Some patience as it takes about 8 hours the first time.

## Steps

### Setup the machine

Execute

`sudo apt-get install gawk wget git-core diffstat unzip texinfo gcc-multilib build-essential chrpath socat libsdl1.2-dev xterm cpio curl`

This will install the necessary packages.

Execute

`export AGL_TOP=$HOME/workspace_agl; mkdir -p $AGL_TOP`

Execute

`mkdir -p ~/bin ; export PATH=~/bin:$PATH ;curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo; chmod a+x ~/bin/repo`

This will set up the repo tool. Repo tool is used to download the recipes for AGL image.

Execute

`cd $AGL_TOP ;repo init -b flounder -m flounder_6.0.1.xml -u https://gerrit.automotivelinux.org/gerrit/AGL/AGL-repo ;repo sync`

This will download the Funky Flounder version of AGL. This version has been tested and is recommended. 

### Start Building

Execute

`source meta-agl/scripts/aglsetup.sh -m raspberrypi3 agl-demo agl-netboot agl-appfw-smack ; bitbake agl-demo-platform`

This will start the build system and would take about 7 hours to complete if you are running for the first time, so you could take a nap :P. The Yocto/bitbake build system has a caching mechanism and hence from the next time on, this would only take a few minutes.


### Adding Kuksa layers

Go to $HOME/workspace_agl/build/conf folder and open bblayers.conf file.

Append the following lines to the end of the file.

```
BBLAYERS =+ “ \

${METADIR}/meta-kuksa \
${METADIR}/meta-virtualization \

“ 
```
Now copy the meta-kuksa folder (Link : https://github.com/eclipse/kuksa.invehicle/agl-kuksa) into the $HOME/workspace_agl directory.

### Configure meta-kuksa layer

The kuksa layer contains recipes for the APIs and Apps contained in Eclipse kuksa Invehicle repo.

The AGL image with meta-kuksa layer adds w3c-visserver-api and elm327-visdatafeeder as systemd services. It will install the datalogger apps in the respective locations `/usr/bin/datalogger-<PROTOCOL>`

#### Set up wifi

--- Ignore this step if wifi is not required ---

With meta-kuksa layer the wifi connection could be set up while building an Image so that the target device connects to the specified wifi, which make it easier to ssh into the device. The wifi settings could be configured by modifying the `meta-kuksa/recipes-devtools/wifi-conf/files/wifi_default.config` file.
Update the "Name" and the "Passphrase" of the wifi you want the device to connect to. More more secured wifi connection please refer to the [link](https://manpages.debian.org/testing/connman/connman-service.config.5.en.html)

#### configure Bluetooth connection with ELM 327 bluetooth adapter

The elm327-datafeeder service connects to an ELM327 Bluetooth adapter to retrieve data from the vehicle. Hence the bluetooth connection with the ELM327 adapter needs to be established before the service starts. The BT connection can be configured by Updating the MAC-Address of the adapter along with its pairing PIN. The MAC-Addr and PIN can be updated in file `meta-kuksa/recipes-elm327-visdatafeeder/elm327-visdatafeeder/files/bt_setup.sh`

Update the fields

![Alt text](./pictures/bt_setup.png?raw=true "bt-setup")
 

Now Execute the below line to build image with Kuksa layers

`source meta-agl/scripts/aglsetup.sh -m raspberrypi3 agl-demo agl-netboot agl-appfw-smack ; bitbake agl-demo-platform`

This would take a few minutes to execute and at the end of the process the bootable image for RaspberryPi 3 will be found in the below location

`$HOME/workspace_agl/build/tmp/deploy/images/raspberrypi3`

### First Launch 

Once the image is ready, burn it onto a SD-card and boot up the image on raspi 3. The w3c-visserver-api requires the vss_rel_1.0.json file to set up the vss tree structure. This file can be copied to the `/usr/bin/w3c-visserver` folder by using scp command (sample file is available under https://github.com/GENIVI/vehicle_signal_specification or could also be generated using the tools in the repo). Once the file has been copied reboot the raspi 3.

### Launch Datalogger apps

The Datalogger apps connect to a remote HONO-Instance and hence the IP-address of the Hono-Instance needs to be updated. The datalogger apps are already installed if you have followed the above steps. Now update the Hono configuration in the file `/usr/bin/datalogger-*/start.sh` with valid IP-address for the respective adapters ( eg: HTTP and MQTT), Port, Device and password for Hono.

And you could start the datalogger apps by executing `./usr/bin/datalogger-*/start.sh`  

The apps connect to the w3c-visserver service using a websocket connection and retrieves Signal.OBD.RPM and Signal.OBD.Speed values to send to hono by packing the retrieved data into a json which looks like this `{SPEED:xxx}` & `{RPM:yyy}`

# Documentation

The official documentation of this project can be reviewed [here](https://agl-kuksa.readthedocs.io/en/latest/) [![Documentation Status](https://readthedocs.org/projects/agl-kuksa/badge/?version=latest)](https://agl-kuksa.readthedocs.io/en/latest/?badge=latest)

