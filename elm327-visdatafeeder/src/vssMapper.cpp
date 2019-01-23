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
#include <json.hpp>


using namespace std;
using namespace jsoncons;

typedef unsigned char UInt8 ; 
typedef unsigned short int UInt16 ;
typedef unsigned long int UInt32 ;
typedef signed char Int8 ;
typedef short int Int16 ;
typedef long int Int32 ;
typedef float Float ;
typedef double Double ;
typedef bool Boolean ;

int tokenizeResponse(char** tokens , string response) {
  char* cString = strdup(response.c_str());
  char *tok = strtok(cString, " ");
  int i = 0;
  while (tok != NULL) {
    tokens[i++] = strdup(tok);
    tok = strtok(NULL, " ");
  }
  free(cString);
  return i;
}

json setRequest(string path) {

  json req;
  req["requestId"] = rand() % 99999;
  req["action"]= "set";
  req["path"] = string(path);
  return req;
}



string setRPM() {

  string readBuf = readMode1Data("01 0C\r");
  int pos = readBuf.find("41 0C", 0);

  if( pos == -1) {
      cout << "Response not valid for RPM" << endl;
      return "Error";
  }

  string response = readBuf.substr (pos, 12);

  if (response.empty()) {
      cout << "RPM Data is NULL form vehicle!" <<endl;
      return "Error";
  }
  
  char* tokens[4];
  tokenizeResponse(tokens , response);

  if(string(tokens[1]) != "0C"){
     cout<< "PID not matching for RPM!" <<endl;
     return "Error";
  }

  int A = stoi (string(tokens[2]),nullptr,16);
  int B = stoi (string(tokens[3]),nullptr,16);
  
  UInt16 value = (A * 256 + B) / 4;
 
  cout << "RPMread from the vehicle = "<< value << endl;

  json req = setRequest("Signal.OBD.RPM"); 
  req["value"] = value;
  stringstream ss; 
  ss << pretty_print(req);
  string resp = ss.str();
  cout << resp << endl;
  return resp;
}

string setVehicleSpeed() {

  string readBuf = readMode1Data("01 0D\r");
  int pos = readBuf.find("41 0D", 0);

  if( pos == -1) {
      cout << "Response not valid for Vehicle Speed " << readBuf <<endl;
      return "Error";
  }

  string response = readBuf.substr (pos, 9);

  if (response.empty()) {
      cout << "Vehicle Speed Data is NULL form vehicle!" <<endl;
      return "Error";
  }
  char* tokens[3];
  tokenizeResponse(tokens , response);

  if(string(tokens[1]) != "0D"){
     cout<< "PID not matching for vehicle speed!" <<endl;
     return "Error";
  }

  int A = stoi (string(tokens[2]),nullptr,16);
 
  Int32 value = A ;
 
  cout << "Vehicle speed read from the vehicle = "<< value << endl;
  json req = setRequest("Signal.OBD.Speed"); 
  req["value"] = value;
  stringstream ss; 
  ss << pretty_print(req);
  string resp = ss.str();
  cout << resp << endl; 
  return resp;
}

string setFuelLevel() {

  string readBuf = readMode1Data("01 2F\r");
  int pos = readBuf.find("41 2F", 0);

  if( pos == -1) {
      cout << "Response not valid for Fuel level" << endl;
      return "Error";
  }

  string response = readBuf.substr (pos, 9);

  if (response.empty()) {
      cout<<"Fuel level Vehicle Speed Data is NULL form vehicle!" <<endl;
      return "Error";
  }
  char* tokens[3];
  tokenizeResponse(tokens , response);

  if(string(tokens[1]) != "2F"){
     cout<< "PID not matching for Fuel level!" <<endl;
     return "Error";
  }

  int A = stoi (string(tokens[2]),nullptr,16);
 
  Int32 value = A ;
 
  cout << "Fuel level read from the vehicle = "<< value << endl;
  json req = setRequest("Signal.OBD.FuelLevel"); 
  req["value"] = value;
  stringstream ss; 
  ss << pretty_print(req);
  string resp = ss.str();
  cout << resp << endl; 
  return resp;
}

string createDTCJson( string dtcCode ) {

  json req;
  if( dtcCode == "0104") {
     req = setRequest("Signal.OBD.DTC1");
     req["value"] = true; 
  } else if( dtcCode == "0105"){
     req = setRequest("Signal.OBD.DTC2");
     req["value"] = true; 
  } else if( dtcCode == "0106"){
     req = setRequest("Signal.OBD.DTC3");
     req["value"] = true; 
  } else if( dtcCode == "0107"){
     req = setRequest("Signal.OBD.DTC4");
     req["value"] = true; 
  } else if( dtcCode == "0108"){
     req = setRequest("Signal.OBD.DTC5");
     req["value"] = true; 
  } else if( dtcCode == "0109"){
     req = setRequest("Signal.OBD.DTC6");
     req["value"] = true; 
  }
  stringstream ss; 
  ss << pretty_print(req);
  string resp = ss.str();
  cout << resp << endl; 
  return resp;
}


list<string> readErrors() {
   
  list<string> errorList;
  string readBuf = readMode3Data();
  int pos = readBuf.find("43", 0);

  if( pos == -1) {
      cout << "Response not valid for Error reading" << endl;
      return errorList;
  }

  string response = readBuf.substr (pos);


  cout << response << endl;
  if (response.empty()) {
      cout << "DTC Data is NULL from vehicle!" <<endl;
      return errorList;
  }
  char* tokens[64];
  int tknos = tokenizeResponse(tokens , response);

  int dtcNos = stoi (string(tokens[1]),nullptr,10);

  cout <<"" << dtcNos << " Errors found" << endl;

  if ( dtcNos > 0) {
       for(int i=0 ; i < dtcNos*2 ; i++) {
          stringstream ss;
          ss << tokens[2 + i];
          i++;
          ss << tokens[2 + i];

          string dtcCode = ss.str();
          errorList.push_back(createDTCJson(dtcCode));
       }
   } else if ( dtcNos == 0) {
      // clear all errors.
      json req;
      req = setRequest("Signal.OBD.*");
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
      cout << resp << endl;
      errorList.push_back(resp);
   }

  return errorList;
}
