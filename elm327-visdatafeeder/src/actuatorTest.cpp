/*
 * ******************************************************************************
 * Copyright (c) 2018 Robert Bosch GmbH and others.
 *
 * All rights reserved. This program and the accompanying materials
 * are made available under the terms of the Eclipse Public License v2.0
 * which accompanies this distribution, and is available at
 * https://www.eclipse.org/org/documents/epl-2.0/index.php
 *
 *  Contributors:
 *      Robert Bosch GmbH - initial API and functionality
 * *****************************************************************************
 */
#include<string>
#include <iostream>
#include "actuatorTest.hpp"
#include "obd.hpp"

using namespace std;



void moveThrottleValve() {
  cout << "sending Throttle Request"<< endl;     
  string resp = writeMode8Data("08 77\r");
  cout <<"Throttle cmd resp= "<< resp << endl;
}
