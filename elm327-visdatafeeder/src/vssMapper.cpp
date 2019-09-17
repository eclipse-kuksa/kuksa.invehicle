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
#include <string.h>
#include <iostream>
#include <json.hpp>
#include "obd.hpp"

using namespace std;
using namespace jsoncons;

typedef unsigned char UInt8;
typedef unsigned short int UInt16;
typedef unsigned long int UInt32;
typedef signed char Int8;
typedef short int Int16;
typedef long int Int32;
typedef float Float;
typedef double Double;
typedef bool Boolean;

// Utility tokenizer.
int tokenizeResponse(string tokens[], const string response) {
  string copy_response = string(response);
  int length = copy_response.length();
  int nos = 0;
  for(int i=0 ; i<length ; i+=2) {
       tokens[nos++] = copy_response.substr(i, 2);
  }
  return nos;
}


// Reads RPM from the vehicle.
int getRPM() {
  string readBuf = readMode1Data("01 0C\r\n");
  int pos = readBuf.find("410C", 0);

  if (pos == -1) {
    cout << "Response " << readBuf << " not valid for RPM" << endl;
    return -1;
  } 

  string response = readBuf.substr(pos);

  if (response.empty()) {
    cout << "RPM Data is NULL form vehicle!" << endl;
    return -1;
  }

  string tokens[32];
  int toknos = tokenizeResponse(tokens, response);

  if (toknos != 4) {
     cout << "The response does not match exactly as expected. Expected 4 tokens got only "<< toknos << endl;
     return -1;
  }

  if (string(tokens[1]) != "0C") {
    cout << "PID not matching for RPM!" << endl;
    return -1;
  }

  int A = stoi(string(tokens[2]), nullptr, 16);
  int B = stoi(string(tokens[3]), nullptr, 16);

  UInt16 value = (A * 256 + B) / 4;
#ifdef DEBUG
  cout << "RPMread from the vehicle = " << value << endl;
#endif
  return value;
}

// Reads Engine speed from the vehicle 
int getVehicleSpeed() {
  string readBuf = readMode1Data("01 0D\r\n");
  int pos = readBuf.find("410D", 0);

  if (pos == -1) {
    cout << "Response " << readBuf << " not valid for Vehicle speed" << endl;
    return -1;
  }

  string response = readBuf.substr(pos, 9);

  if (response.empty()) {
    cout << "Vehicle Speed Data is NULL form vehicle!" << endl;
    return -1;
  }
  string tokens[32];
  int toknos = tokenizeResponse(tokens, response);

  if (toknos != 3) {
     cout << "The response does not match exactly as expected. Expected 3 tokens got only "<< toknos << endl;
     return -1;
  }

  if (string(tokens[1]) != "0D") {
    cout << "PID not matching for vehicle speed!" << endl;
    return -1;
  }

  int A = stoi(tokens[2], nullptr, 16);

  Int32 value = A;
#ifdef DEBUG
  cout << "Vehicle speed read from the vehicle = " << value << endl;
#endif
  return value;
}

// Reads Fuel status from the vehicle.
int getFuelLevel() {
  string readBuf = readMode1Data("01 2F\r\n");
  int pos = readBuf.find("412F", 0);

  if (pos == -1) {
    cout << "Response not valid for Fuel level" << endl;
    return -1;
  }

  string response = readBuf.substr(pos, 9);

  if (response.empty()) {
    cout << "Fuel level Data is NULL form vehicle!" << endl;
    return -1;
  }
  string tokens[32];
  tokenizeResponse(tokens, response);

  if (tokens[1] != "2F") {
    cout << "PID not matching for Fuel level!" << endl;
    return -1;
  }

  int A = stoi(tokens[2], nullptr, 16);

  Int32 value = A;
  value = (value * 100) / 255;
#ifdef DEBUG
  cout << "Fuel level read from the vehicle = " << value << endl;
#endif
  return value;
}

// Utility method to create W3C-VIS SET request
json setRequest(string path) {
  json req;
  req["requestId"] = rand() % 99999;
  req["action"] = "set";
  req["path"] = string(path);
  return req;
}

// Reads RPM from the vehicle and packs the response in w3c-VIS SET request.
string setRPM() {
  UInt16 value = getRPM();
#ifdef DEBUG
  cout << "RPMread from the vehicle = " << value << endl;
#endif

  json req = setRequest("Vehicle.OBD.EngineSpeed");
  req["value"] = value;
  stringstream ss;
  ss << pretty_print(req);
  string resp = ss.str();
  return resp;
}

// Reads Engine speed from the vehicle and packs the response in w3c-VIS SET
// request.
string setVehicleSpeed() {

  Int32 value = getVehicleSpeed();
#ifdef DEBUG
  cout << "Vehicle speed read from the vehicle = " << value << endl;
#endif
  json req = setRequest("Vehicle.OBD.Speed");
  req["value"] = value;
  stringstream ss;
  ss << pretty_print(req);
  string resp = ss.str();
  cout << resp << endl;
  return resp;
}

// Reads Fuel status from the vehicle and packs the response in w3c-VIS SET
// request.
string setFuelLevel() {

  Int32 value = getFuelLevel();
#ifdef DEBUG
  cout << "Fuel level read from the vehicle = " << value << endl;
#endif
  json req = setRequest("Vehicle.OBD.FuelLevel");
  req["value"] = value;
  stringstream ss;
  ss << pretty_print(req);
  string resp = ss.str();
  cout << resp << endl;
  return resp;
}

// Utility method to pack DTC data in W3C-VIS SET format.
string createDTCJson(string dtcCode) {
  json req;
  if (dtcCode == "0104") {
    req = setRequest("Vehicle.OBD.DTC1");
    req["value"] = true;
  } else if (dtcCode == "0105") {
    req = setRequest("Vehicle.OBD.DTC2");
    req["value"] = true;
  } else if (dtcCode == "0106") {
    req = setRequest("Vehicle.OBD.DTC3");
    req["value"] = true;
  } else if (dtcCode == "0107") {
    req = setRequest("Vehicle.OBD.DTC4");
    req["value"] = true;
  } else if (dtcCode == "0108") {
    req = setRequest("Vehicle.OBD.DTC5");
    req["value"] = true;
  } else if (dtcCode == "0109") {
    req = setRequest("Vehicle.OBD.DTC6");
    req["value"] = true;
  }
  stringstream ss;
  ss << pretty_print(req);
  string resp = ss.str();
#ifdef DEBUG
  cout << resp << endl;
#endif
  return resp;
}

// Reads DTCs from the vehicle and packs the response in w3c-VIS SET request.
// Updates 6 DTCs in VSS tree (0104, 0105, 0106, 0107, 0108 and 0109). These are
// some dummy values.
list<string> readErrors() {
  list<string> errorList;
  string readBuf = readMode3Data();
  int pos = readBuf.find("43", 0);

  if (pos == -1) {
    cout << "Response not valid for Error reading" << endl;
    return errorList;
  }

  string response = readBuf.substr(pos);

  cout << response << endl;
  if (response.empty()) {
    cout << "DTC Data is NULL from vehicle!" << endl;
    return errorList;
  }
  string tokens[64];
  int tknos = tokenizeResponse(tokens, response);

  int dtcNos = stoi(string(tokens[1]), nullptr, 10);
#ifdef DEBUG
  cout << "" << dtcNos << " Errors found" << endl;
#endif

  if (dtcNos > 0) {
    for (int i = 0; i < dtcNos * 2; i++) {
      stringstream ss;
      ss << tokens[2 + i];
      i++;
      ss << tokens[2 + i];

      string dtcCode = ss.str();
      errorList.push_back(createDTCJson(dtcCode));
    }
  } else if (dtcNos == 0) {
    // clear all errors.
    json req;
    req = setRequest("Vehicle.OBD.*");
    json array = json::array();
    json dtc1;
    dtc1["DTC1"] = false;
    array.push_back(dtc1);
    json dtc2;
    dtc2["DTC2"] = false;
    array.push_back(dtc2);
    json dtc3;
    dtc3["DTC3"] = false;
    array.push_back(dtc3);
    json dtc4;
    dtc4["DTC4"] = false;
    array.push_back(dtc4);
    json dtc5;
    dtc5["DTC5"] = false;
    array.push_back(dtc5);
    json dtc6;
    dtc6["DTC6"] = false;
    array.push_back(dtc6);

    req["value"] = array;
    stringstream ss;
    ss << pretty_print(req);
    string resp = ss.str();
#ifdef DEBUG
    cout << resp << endl;
#endif
    errorList.push_back(resp);
  }

  return errorList;
}
