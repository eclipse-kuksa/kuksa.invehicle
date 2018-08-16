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
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <iostream>
#include <unistd.h>
#include "client_wss.hpp"
#include "honoHTTP.hpp"
#include <json.hpp>


using namespace std;

using WssClient = SimpleWeb::SocketClient<SimpleWeb::WSS>;
using namespace jsoncons;

bool honoConnect = true;

char honoAddress[256];
int  honoPort;
char honoDevice[256];
char honoPassword[256];

char TOKEN[2048];

const string DEFAULT_TENANT = "DEFAULT_TENANT";

std::string query;

string url = "localhost:8090/vss";

shared_ptr<WssClient::Connection> connection = NULL;


void sendToHono( string resp) {

    cout << "Response >> " << resp << endl;
    json root;
    root = json::parse(resp);
    string action = root["action"].as<string>();
    
    if( action == "authorize") {
        return;
    } else if ( root.has_key("error")) {
        cout << " Error response from server " <<  root["error"].as<string>() << endl;
        return;
    }

     
      
    std::string value = root["value"].as<string>();
    int val = stoi(value, nullptr, 10);   
    int reqID = root["requestId"].as<int>();
    string signal;
    if(reqID == 1234) {
       signal = "RPM";
    } else if (reqID == 1235) {
       signal = "SPEED";
    } 

   // int status = sendTelemetryDataToHonoInstance (honoAddress, honoPort, (char*) DEFAULT_TENANT.c_str(), honoDevice, honoPassword, (char*)signal.c_str(), val);
      int status = 1;
    if (status == 1) {
        cout << "Message accepted by HONO"<< endl;
    } else {
        cerr << "Message not accepted by HONO"<< endl;
    }
}


void* honoConnectRun (void* arg) {

  if(honoConnect) {
  // wait for 10 seconds.
  usleep(1000000);
  auto send_stream = make_shared<WssClient::SendStream>();

  // send Authorize request.
   json authreq;
   authreq["requestId"] = rand() % 999999;
   authreq["action"]= "authorize";
   authreq["tokens"] = string(TOKEN);
   stringstream ss; 
   ss << pretty_print(authreq);
   *send_stream << ss.str();
   connection->send(send_stream); 

   usleep(1000000);

  // send data to hono instance.
  while(1) {
    
    string rpm_req = "{\"action\": \"get\", \"path\": \"Signal.OBD.EngineSpeed\", \"requestId\": 1234 }";

    
    *send_stream << rpm_req;
    connection->send(send_stream);    



     // sleep 1 sec
    usleep(1000000);  
    string vSpeed_req = "{\"action\": \"get\", \"path\": \"Signal.OBD.Speed\", \"requestId\": 1235 }";
    
    *send_stream << vSpeed_req;
    connection->send(send_stream); 

    
    
     // sleep 1 sec
    usleep(1000000);
  }
 }
}

void* startWSClient(void * arg) {

  WssClient client(url , true, "Client.pem", "Client.key", "CA.pem");

  client.on_message = [](shared_ptr<WssClient::Connection> connection, shared_ptr<WssClient::Message> message) {
    sendToHono(message->string());
  };

  client.on_open = [](shared_ptr<WssClient::Connection> conn) {
    cout << "Connection with server at " << url << " opened" << endl;
    connection = conn;
       pthread_t honoConnect_thread;
        /* create the hono connection thread. */
        if(pthread_create(&honoConnect_thread, NULL, &honoConnectRun, NULL )) {

         cout<<"Error creating hono connect run thread"<<endl;
         return 1;

        }
  };

  client.on_close = [](shared_ptr<WssClient::Connection> /*connection*/, int status, const string & /*reason*/) {
    cout << "Connection closed with status code " << status << endl;
    connection = NULL;
  };

  // See http://www.boost.org/doc/libs/1_55_0/doc/html/boost_asio/reference.html, Error Codes for error code meanings
  client.on_error = [](shared_ptr<WssClient::Connection> /*connection*/, const SimpleWeb::error_code &ec) {
    cout << "Error: " << ec << ", message: " << ec.message() << endl;
  };

   client.start();
}





/**
 * @brief  Test main.
 * @return
 */
int main(int argc, char* argv[])
{

        if(argc == 6) {
           strcpy(honoAddress , argv[1]);
           char honoPortStr[16];
           strcpy(honoPortStr , argv[2]);
           honoPort = stoi(honoPortStr, nullptr, 10); 
           strcpy(honoPassword , argv[3]); 
           strcpy(honoDevice , argv[4]);
           strcpy(TOKEN, argv[5]);
        } else {
           cerr<<"Usage ./vehicle2cloud <HONO IP-ADDR> <HONO PORT> <HONO-PASSWORD> <HONO-DEVICE NAME> <JWT TOKEN>"<<endl;
           return -1; 
        }

        
       
     pthread_t startWSClient_thread;

        /* create the web socket client thread. */
        if(pthread_create(&startWSClient_thread, NULL, &startWSClient, NULL )) {

         cout << "Error creating websocket client run thread"<<endl;
         return 1;

        }

   getchar();
}



