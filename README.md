<!--
******************************************************************************
Copyright (c) 2018 Dortmund University of Applied Sciences and Arts

All rights reserved. This program and the accompanying materials
are made available under the terms of the Eclipse Public License v2.0
which accompanies this distribution, and is available at
https://www.eclipse.org/org/documents/epl-2.0/index.php

Contributors:
    Robert Hoettger - initial readme files added
*****************************************************************************
-->

# Kuksa-InVehicle Repo

 ![Alt text](./logos/kuksa.png?raw=true "Eclipse kuksa logo")

[Eclipse Kuksa](https://www.eclipse.org/kuksa/) includes an open and secure cloud platform that interconnects a wide range of vehicles to the cloud via open in-car and Internet connection and is supported by an integrated open source software development ecosystem. The Eclipse Kuksa project conatins a set of repositories and this repo is one among those that contains in-vehicle platform code and also contains required layers and bindings to build a Kuksa adapted AGL (Automotive Grade Linux) distribution. The in-vehicle platform is primarily designed to work with AGL. However the individual components found in this repo could be used on other platforms as well.



## Projects

* *agl-kuksa* - Scripts to automate AGL build system with the meta-kuksa layers.
* *elm327-visdatafeeder* - ELM 327 app that reads OBDII data from the vehicle and feeds data to the w3c-visserver.
* *kuksa-hawkbit* - Barebone API for connecting with Hawkbit. Will be shortly replaced with kuksa-appmanager.
* *w3c-visserver-api* - W3C Vehicle Information Specification API.
* *direct-access-api* - Enables sending CAN messages from the cloud to vehicle using Websocket.
* *datalogger-http* - Example app that sends data from the vehicle to an Eclipse Hono instance with http.
* *datalogger-mqtt* - Example app that sends data from the vehicle to an Eclipse Hono instance with mqtt.
* *remoteAccess* - Example app that subscribes to control topic with Hono and receives commands sent.
* *kuksa-appmanager* - Hawkbit appmanager which deploys in-vehicle apps as docker conatiners and more..
* *email-notifier* - Example app that talks to an email-server and sends e-mails to the configured email address. Used at the moment only for internal demos.

## How to build and run AGL-Kuksa on Raspberry Pi 3

Click [here](https://github.com/eclipse/kuksa.invehicle/tree/master/agl-kuksa) to learn more. 


## Get in Touch

Please check out the [Eclipse Kuksa project home page](https://www.eclipse.org/kuksa/) for details regarding our mailing list.
