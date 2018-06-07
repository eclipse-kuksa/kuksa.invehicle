..
  # ******************************************************************************
  # Copyright (c) 2018 Dortmund University of Applied Sciences and Arts
  #
  # All rights reserved. This program and the accompanying materials
  # are made available under the terms of the Eclipse Public License v2.0
  # which accompanies this distribution, and is available at
  # https://www.eclipse.org/org/documents/epl-2.0/index.php
  #
  #  Contributors:
  #      Pedro Cuadra - initial doc
  # *****************************************************************************


.. AGL Kuksa documentation master file, created by
   sphinx-quickstart on Mon Dec 11 20:09:47 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Developers Guide
================

Yocto-based build system generates the;

* *Image:* is the Linux distribution image to be set deployed to the target
  system.
* *SDK:* is a set of libraries, binaries, headers and scripts to enable
  development of applications to be deployed on the Linux distribution running
  on the target.

Pre-built Images/SDK
--------------------

Pre-build images and SDK are provided
`here <https://owncloud.idial.institute/s/7fh4gbQjS7wfN4B>`_.

.. note::
  AGL-kuksa provides two sets of image/SDK one for the Rover and one for the
  plain board, which is Raspberry Pi 3 by default.


Build an Image/SDK
------------------

To build the Image/SDK, run;

.. code-block:: shell

  cd <agl-kuksa-root>
  mkdir build
  cd build
  cmake ..
  make <agl-kuksa-target>

Where `<agl-kuksa-target>` can be;

* `agl-kuksa-image`: AGL kuksa image
* `agl-kuksa-sdk`: AGL kuksa SDK
* `agl-kuksa`: AGL kuksa image and SDK
* `agl-rover-image`: AGL Rover image
* `agl-rover-sdk`: AGL Rover SDK
* `agl-rover`: AGL Rover image and SDK

.. note::
  The output images can be seen at `<agl-kuksa-root>/build/images` and the
  SDKs at `<agl-kuksa-root>/build/sdk`.

Booting the Image
-----------------

To boot the image we recommend to use `Etcher <https://etcher.io/>`_. You can
directly download it from `https://etcher.io/ <https://etcher.io/>`_.

Etcher is a cross platform and straightforward tool for burning Images into SD
cards. First you'll need to select the image you want to burn by clicking on
*Select Image*. This will open a file browser where you can choose your recently
dowloaded or builded `*.rpi-sdimg.xz`.

If you have your SD card already inserted in your PC and it's the only SD card
inserted it will automatically detect it and skip till the last step. If not
just click on *Select Drive* and select your SD card.

After selecting the SD card to be used just click on *Flash!* to start the
burning process. This could take several minutes. Onces it finishes a message
will pop-up saying the image was successfully burned.

Using the SDK
-------------

To use the SDK you need first to install it by running;

.. code-block:: shell

  chmod u+x <target>-glibc-x86_64-agl-demo-platform-crosssdk-armv7vehf-neon-vfpv4-toolchain-<version>.sh
  ./<target>-glibc-x86_64-agl-demo-platform-crosssdk-armv7vehf-neon-vfpv4-toolchain-<version>.sh

.. note::

  The installation script will ask for instalation directory. It's a good idea
  to use the default installation path (`/opt/<target>/<version>`).

Command Line
++++++++++++

Now to cross-compile an application using the command line first need to
source the development environment by running;

.. code-block:: shell

  source /opt/<target>/<version>/environment-setup-armv7vehf-neon-vfpv4-rover-linux-gnueabi

Now you can normally compile your code using the sourced environment.

.. note::
  If your are compiling a `cmake` project you'll need to re-run cmake command
  in order to properly use the sourced environment.


Eclipse Che
+++++++++++

To be Written
