/*
 * Copyright (c) 2017 FH Dortmund and others
 * All rights reserved. This program and the accompanying materials
 * are made available under the terms of the Eclipse Public License v1.0
 * which accompanies this distribution, and is available at
 * http://www.eclipse.org/legal/epl-v10.html
 *
 * Description:
 *    Hono interaction library for Rover - Header file
 *
 * Authors:
 *    M. Ozcelikors,            R.Hottger
 *    <mozcelikors@gmail.com>   <robert.hoettger@fh-dortmund.de>
 *
 */
#include<stdio.h>

using namespace std;

int registerDeviceToHonoInstance (char * host_name, int port, char * tenant_name, char * device_id);
int sendTelemetryDataToHonoInstance (char * host_name, int port, char * tenant_name, char * user, char * password, char * field, double value);
int sendEventDataToHonoInstance (char * host_name, int port, char * tenant_name, char * device_id, char * user, char * password, char * field, double value);
