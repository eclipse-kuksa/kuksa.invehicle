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
#include "vssMapper.hpp"
#include "obd.hpp"
#include <string.h>
#include <iostream>

using namespace std;

void tokenizeResponse(char** tokens , string response) {
  char* cString = strdup(response.c_str());
  char *tok = strtok(cString, " ");
  int i = 0;
  while (tok != NULL) {
    tokens[i++] = strdup(tok);
    tok = strtok(NULL, " ");
  }
  free(cString);
}

void setRPM() {

  string readBuf = readMode1Data("01 0C\r");
  int pos = readBuf.find("41 0C", 0);

  if( pos == -1) {
      cout << "Response not valid for RPM" << endl;
      return;
  }

  string response = readBuf.substr (pos, 12);

  if (response.empty()) {
      cout << "Data is NULL form vehicle!" <<endl;
      return;
  }
  
  char* tokens[4];
  tokenizeResponse(tokens , response);

  if(string(tokens[1]) != "0C"){
     cout<< "PID not matching for RPM!" <<endl;
     return;
  }

  int A = stoi (string(tokens[2]),nullptr,16);
  int B = stoi (string(tokens[3]),nullptr,16);
  
  UInt16 value = (A * 256 + B) / 4;
 
  cout << "RPMread from the vehicle = "<< value << endl;
  setValue(58 , &value);
}

void setVehicleSpeed() {

  string readBuf = readMode1Data("01 0D\r");
  int pos = readBuf.find("41 0D", 0);

  if( pos == -1) {
      cout << "Response not valid for Vehicle Speed" << endl;
      return;
  }

  string response = readBuf.substr (pos, 9);

  if (response.empty()) {
      cout << "Data is NULL form vehicle!" <<endl;
      return;
  }
  char* tokens[3];
  tokenizeResponse(tokens , response);

  if(string(tokens[1]) != "0D"){
     cout<< "PID not matching for vehicle speed!" <<endl;
     return;
  }

  int A = stoi (string(tokens[2]),nullptr,16);
 
  Int32 value = A ;
 
  cout << "Vehicle speed read from the vehicle = "<< value << endl;
  setValue(48 , &value);

}
