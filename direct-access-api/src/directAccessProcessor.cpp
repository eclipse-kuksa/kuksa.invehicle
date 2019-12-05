/*
 * ******************************************************************************
 * Copyright (c) 2018 Robert Bosch GmbH.
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

#include "directAccessProcessor.hpp"
#include <iostream>
#include <sstream>
#include <stdint.h>
#include "Simple-WebSocket-Server/server_ws.hpp"
#include "visconf.hpp"
#include "exception.hpp"

using namespace std;

directAccessProcessor::directAccessProcessor(class authenticator* vdator) {
  tokenValidator = vdator;
  accessValidator = new accesschecker(tokenValidator);
  vcanHandler = new vcanhandler();
}

string directAccessProcessor::processCreate(json perm_json, string rchannel) {


  string vcan = vcanHandler->createVcan();

  if (vcan == "-1") {  // failed to create vcan
    json result;
    json error;
    result["action"] = "create";
    error["reason"] = "Failed to create VCAN";
    result["error"] = error;
    result["timestamp"] = time(NULL);

    std::stringstream ss;
    ss << pretty_print(result);
    return ss.str();
  }

  // create vcan entry on db
  dbmanager db;
  db.insert_into_vcan_table(vcan);

  // set read/write permissions
  json can_json = perm_json["roles"];

  db.store_read_rules(vcan, can_json);
  db.store_write_rules(vcan, can_json);


  // start vcan listener
  vcanHandler->start_vcan_listener(vcan);

  json res;
  res["action"] = "create";
  res["vcan"] = vcan;
  res["rcan"] = rchannel;
  res["timestamp"] = time(NULL);
  stringstream ss;
  ss << pretty_print(res);
  cout << " Created VCAN Channel " << res["vcan"].as<string>()
       << " for Real CAN " << rchannel
       << " with access on : " << can_json << endl;
  return ss.str();

}

string directAccessProcessor::processDelete(string vchannel) {
  json answer;

  answer["action"] = "delete";
  answer["timestamp"] = time(NULL);

  if (vcanHandler->vcanExists(vchannel) == false) {
    json error;
    answer["action"] = "delete";
    error["reason"] = vchannel + " does not exist.";
    answer["error"] = error;
    answer["timestamp"] = time(NULL);
  }

  // delete vcan
  vcanHandler->deleteVcan(vchannel);

  // delete from db
  dbmanager db;
  db.delete_vcan(vchannel);

  answer["vcan"] = vchannel;


  std::stringstream ss;
  ss << pretty_print(answer);
  return ss.str();
}


string directAccessProcessor::processQuery(string req_json,
                                           class wschannel& channel) {

  json result;
  json error;
  json root;
  root = json::parse(req_json);
  string action = root["action"].as<string>();
  string clientid = root["appid"].as<string>();
  string secret = root["secret"].as<string>();

  root["daaid"] = "daa_client";
  root["daasecret"] = "5f84495a-72f0-4414-be4f-5eec082e5732";
  root["api"] = "1";

  cout << "incoming: " << root << endl;

  // create socket
  int sockfd = socket(AF_UNIX, SOCK_STREAM, 0);
  if (sockfd < 0) {
    printf("Failed to create AF_UNIX socket\n");
    error["message"] = "Failed to process request.";
    result["error"] = error;
    result["timestamp"] = time(NULL);

    std::stringstream ss;
    ss << pretty_print(result);
    return ss.str();
  }
  struct sockaddr_un addr;

  memset(&addr, '0', sizeof(addr));
  addr.sun_family = AF_UNIX;
  strncpy(addr.sun_path, perm_mngt_srv_address.c_str(), sizeof(addr.sun_path)-1);

  // connect
  int conn_status = connect(sockfd, (struct sockaddr*)&addr, sizeof(addr));
  if (conn_status < 0) {
    printf("Failed to connect to permission mngt server: %d\n", conn_status);
    error["message"] = "Failed to process request.";
    result["error"] = error;
    result["timestamp"] = time(NULL);

    std::stringstream ss;
    ss << pretty_print(result);
    return ss.str();
  }
  printf("Connected to permission mngt server\n");

  char buffer[PERM_MNGT_BUFFER_SIZE] = {};

  memset(&buffer, '\0', sizeof(buffer));

  string jsonstr;
  root.dump(jsonstr);
  char *msg = &jsonstr[0];

  if (write(sockfd, msg, strlen(msg)) < 0){
    printf("Failed to send request to permission mngt server\n");
    error["message"] = "Failed to process request.";
    result["error"] = error;
    result["timestamp"] = time(NULL);

    std::stringstream ss;
    ss << pretty_print(result);
    return ss.str();

  }else{
    printf("sent\n");

    int r = read(sockfd, buffer, PERM_MNGT_BUFFER_SIZE);
    if (r < 0) {
      printf("Failed to read from permission mngt server\n");
    } else if (r == 0) {
      printf("Disconnected from permission mngt server \n");
      connection_status = -1;
    } else {
      printf("permission mngt: %s\n", buffer);

      try{
        //parse response
        json perm_json = json::parse(buffer);

        if (action == "create") {
          cout << "directAccessProcessor::processQuery: Create action: " << action << endl;
          string can_channel = root["channel"].as<string>();
          result = processCreate(perm_json, can_channel);
        } else if (action == "delete") {
          cout << "directAccessProcessor::processQuery: Delete action: " << action << endl;
          string vcan_channel = root["vchannel"].as<string>();
          result = processDelete(vcan_channel);
        } else {
           cout << "vsscommandprocessor::processQuery: Unknown action: " << action << endl;
           error["message"] = "Unknown action";
           result["error"] = error;
           result["timestamp"] = time(NULL);

        }
      }
      catch(...){
        cout << "Exception occured trying to handle permission mngt response "<< endl;

        error["message"] = "Failed to process request.";
        result["error"] = error;
        result["timestamp"] = time(NULL);
      }

      memset(&buffer, '\0', sizeof(buffer));
      std::stringstream ss;
      ss << pretty_print(result);
      return ss.str();
    }

  }

}
