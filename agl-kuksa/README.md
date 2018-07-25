# AGL KUKSA

Kuksa is a wrapper project around Automotive Grade Linux (AGL). From its side,
AGL uses Yocto/Bitbake building system to build an automotive domain specific
Linux distribution. Therefore, this projects provides a building system that
adds Kuksa's specific Bitbake layers on top of the original AGL. The scripts in 
this project help ease the process of building an AGL image by simple using a few
commands. This project includes the yocto recipes found in meta-kuksa project.

# Prerequisites

* PC with a Linux Distro (eg: ubuntu).
* Minimum of 100GB Memory.
* Some patience as it takes about 8 hours the first time.

# Dependencies

To be able to build this AGL image first install the building dependencies by
running;

```
  apt install cmake curl chrpath build-essential texinfo
```

# Build the Image/SDK with cmake scripts

--- not stable as yet use steps mentioned in the next section ---

## Prerequisites:

1. Need Ubuntu 16

2. Fast Internet connection.

3. Minimum of 100 GB memory.

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

## Steps

### Setup the machine

Execute

`sudo apt-get install gawk wget git-core diffstat unzip texinfo gcc- multilib build-essential chrpath socat libsdl1.2-dev xterm cpio curl`

This will install the necessary packages.

Execute

`export AGL_TOP=$HOME/workspace_agl; mkdir -p $AGL_TOP`

Execute

`mkdir -p ~/bin ; export PATH=~/bin:$PATH ;curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo; chmod a+x ~/bin/repo`

This will set up the repo tool. Repo tool is used to download the recipes for AGL image.

Execute

`cd $AGL_TOP ;repo init -b dab -u https://gerrit.automotivelinux.org/gerrit/AGL/AGL-repo ;repo sync`

This will download the latest daring dab version of AGL.

### Start Building

Execute

`source meta-agl/scripts/aglsetup.sh -m raspberrypi3 agl-demo agl-netboot agl-appfw-smack ; bitbake agl-demo-platform`

This will start the build system and would take about 7 hours to complete if you are running for the first time, so you could take a nap :P. The Yocto/bitbake build system has a caching mechanism and hence from the next time on, this would only take a few minutes.

### Adding Kuksa layers

Go to $HOME/workspace_agl/build/conf folder and open bblayers.conf file.

Append the below line at the end of the file.

```
BBLAYERS =+ “ \

${METADIR}/meta-kuksa \

“ 
```
Now copy the meta-kuksa folder (Link : https://github.com/eclipse/kuksa.invehicle/agl-kuksa) into the $HOME/workspace_agl directory.

Now Execute the below line to build image with Kuksa layers

`source meta-agl/scripts/aglsetup.sh -m raspberrypi3 agl-demo agl-netboot agl-appfw-smack ; bitbake agl-demo-platform`

This would take a few minutes to execute and at the end of the process the bootable image for RaspberryPi 3 will be found in the below location

`$HOME/workspace_agl/build/tmp/deploy/images/raspberrypi3` 

# Documentation

The official documentation of this project can be reviewed [here](https://gitlab-pages.idial.institute/appstacle/agl-kuksa/index.html).
