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

Layers Definition
=================

To follow Yocto/Bitbake building system's architecture, further modifications
to the AGL Image/SDK are done using Bitbake layers on top. Kuksa related layers
have lower priority than AGL's to guarantee that Kuksa's layers are in fact
added on top of AGL's.

.. note::
  For more information regarding Bitbake Layers priorities please review the
  usage of `BBFILE_PRIORITY` in the `Bitbake User Manual
  <https://www.yoctoproject.org/docs/1.6/bitbake-user-manual/bitbake-user-manual.html>`_

meta-kuksa layer
----------------

The `meta-kuksa` layer shall contain all packages needed for the APPSTACLE
project that aren't already included in AGL. Furthermore, here is were
the APPSTACLE project's code base could be added into the Image/SDK.

meta-kuksa-dev layer
--------------------

The `meta-kuksa-dev` layer contains all extra packages that are useful for
the development process but aren't required in the production Image.

meta-rover layer
----------------

This layer holds all the needed packages to enable the development for the
Rover. Basically, it provides
`rover-app <https://github.com/app4mc-rover/rover-app>`_,
`rover-web <https://github.com/app4mc-rover/rover-web>`_ and all their
dependencies.

.. note::
  For more information regarding the Rover's internal please review the
  `APP4MC-Rover Documentation <https://app4mc-rover.github.io/rover-docs/>`_.
