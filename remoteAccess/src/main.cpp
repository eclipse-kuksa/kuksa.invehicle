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
#include "honoMqtt.hpp"
#include <json.hpp>


using namespace std;

using WssClient = SimpleWeb::SocketClient<SimpleWeb::WSS>;
using namespace jsoncons;
using jsoncons::json;

std::string query;

string url = "localhost:8090/vss";

bool honoConnect = true;

char honoAddress[256];
char honoPort[32];
char honoDevice[256];
char honoPassword[256];

char TOKEN[2048];
shared_ptr<WssClient::Connection> connection = NULL;


const std::string CLIENT_ID { "remoteAccess" };

const string SUB_TOPIC { "control/+/+/req/#" };
const string PUB_TOPIC {"telemetry"};
const int QOS = 0;

const auto TIMEOUT = std::chrono::seconds(10);

class HonoMqtt* honoConn;

void sendRequest(string command) {
   cout << "Send << " << command <<endl;     
   auto send_stream = make_shared<WssClient::SendStream>();
   *send_stream << command;
   connection->send(send_stream);
}

// callback method for receiving messages from hono.
void onMessageFromHono(string message) {

   json msg;
   msg = json::parse(message);
   
   if( !msg.has_key("command")) {
      cout << "Malformed command received from hono" << endl;
   } else if(msg["command"].as<string>() == "k") {
      cout << "Command received from Hono" << message << endl;
      json req;
      req["requestId"] = rand() % 99999;
      req["action"]= "set";
      req["path"] = "Signal.Drivetrain.InternalCombustionEngine.ThrottleTest";
      req["value"] = 100;
      stringstream ss; 
      ss << pretty_print(req);
      sendRequest(ss.str());
   } else {
     cout << "Invalid command received from hono" << endl;
   }
}


void* honoConnectRun (void* arg) {

  if(honoConnect) {
  // wait for 1 second.
  usleep(100000);
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


   string honoAddr = string(honoAddress) +":" + string(honoPort);
   honoConn = new HonoMqtt();
   try {
      cout << honoAddr <<endl;
      string userName = string(honoDevice) + "@DEFAULT_TENANT";
      string password(honoPassword);
      honoConn->connect(honoAddr, CLIENT_ID, userName, password);
      honoConn->setMessageCB(onMessageFromHono);
      usleep(2000000);
      honoConn->subscribe(SUB_TOPIC);
   } catch ( mqtt::exception& e) {

   }

  // send data to hono instance.
  while(1) {
     // sleep 0.5 sec
    usleep(500000);
  }
 }
}

void* startWSClient(void * arg) {

  WssClient client(url , true, "Client.pem", "Client.key", "CA.pem");

  client.on_message = [](shared_ptr<WssClient::Connection> connection, shared_ptr<WssClient::Message> message) {
   
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
           strcpy(honoPort , argv[2]);
           strcpy(honoPassword , argv[3]); 
           strcpy(honoDevice , argv[4]);
           strcpy(TOKEN, argv[5]);
        } else {
           cerr<<"Usage ./remoteAccess <HONO-MQTT IP-ADDR> <HONO-MQTT PORT> <HONO-PASSWORD> <HONO-DEVICE NAME> <JWT TOKEN>"<<endl;
           return -1; 
        }

        
       
     pthread_t startWSClient_thread;

        /* create the web socket client thread. */
        if(pthread_create(&startWSClient_thread, NULL, &startWSClient, NULL )) {

         cout << "Error creating websocket client run thread"<<endl;
         return 1;

        }
while (1) { usleep (1000000); };
}



