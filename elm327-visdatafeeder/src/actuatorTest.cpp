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



void moveThrottleValve(int percent) {
  cout << "sending Throttle Request for % " << percent << endl; 
  string command = "\r";
  switch (percent) {

     case 25:
              command = "08 77 19\r";
              break;
     case 50:
              command = "08 77 32\r";
              break;

     case 75: 
              command = "08 77 4b\r";
              break;
 
     case 100:
              command = "08 77 64\r";
              break;

  }    
  string resp = writeMode8Data(command);
  cout <<"Throttle cmd resp= "<< resp << endl;
}


