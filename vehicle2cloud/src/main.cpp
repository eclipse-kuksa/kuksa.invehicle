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

#include "vss.hpp"
#include "vssserializer.hpp"
#include "vsscommandprocessor.hpp"
#include "vssdatabase.hpp"
#include "visconf.hpp"
#include "server_ws.hpp"
#include "vssMapper.hpp"
#include "obd.hpp"
#include "honoHTTP.hpp"
#include <json.hpp>


using namespace std;


bool honoConnect = true;

char honoAddress[256];
int honoPort;
char PORT[128];
char honoDevice[256];
char honoPassword[256];

const string DEFAULT_TENANT = "DEFAULT_TENANT";

int connectionHandle = -1;

using WsServer = SimpleWeb::SocketServer<SimpleWeb::WS>;


uint16_t connections[MAX_CLIENTS + 1] = {0};

std::string query;
WsServer server;


struct node mainNode;
struct signal* ptrToSignals[MAX_SIGNALS];
UInt32 subscribeHandle[MAX_SIGNALS][MAX_CLIENTS];


uint32_t generateConnID() {
 uint32_t  retValueValue = 0;
   for(int i=1 ; i<(MAX_CLIENTS + 1) ; i++) {
     if(connections[i] == 0) {
         connections[i]= i;
         retValueValue = CLIENT_MASK * (i);
         return retValueValue;
     } 
  }
    return retValueValue;
}


void sendToHono( string resp , string signal) {

    json root;
    root = json::parse(resp);
    std::string value = root["value"].as<string>();
    int val = stoi(value, nullptr, 10);    

    int status = sendTelemetryDataToHonoInstance (honoAddress, honoPort, (char*) DEFAULT_TENANT.c_str(), honoDevice, honoPassword, (char*)signal.c_str(), val);

    if (status == 1) {
        cout << "Message accepted by HONO"<< endl;
    } else {
        cerr << "Message not accepted by HONO"<< endl;
    }

}


void* honoConnectRun (void* arg) {

  if(honoConnect) {
  // wait for 10 seconds.
  usleep(10000000);

  // send data to hono instance.
  while(1) {
    
    string rpm_req = "{\"action\": \"get\", \"path\": \"Signal.Drivetrain.InternalCombustionEngine.RPM\", \"requestId\": 1234 }";
    string rpm_resp = processQuery(rpm_req, 0);
    sendToHono(rpm_resp , "RPM");


    string vSpeed_req = "{\"action\": \"get\", \"path\": \"Signal.Vehicle.Speed\", \"requestId\": 1235 }";
    string vSpeed_resp = processQuery(vSpeed_req, 0);
    sendToHono(vSpeed_resp , "SPEED");
    
     // sleep 1 sec
    usleep(1000000);
  }
 }
}



// Thread that updates the tree.
void* elmRun (void* arg) {
 connectOBD(10);

  usleep(1000000);
  // Punp the data into the tree.
 while(1) {
    // sleep 1 sec
    usleep(1000000);
    setRPM();
    setVehicleSpeed();
  }
}

// Thread that starts the WS server.
void* startWSServer(void * arg) {

   cout<<"starting WS server"<<endl;
           
   server.config.port = 8090;

   auto &vssEndpoint = server.endpoint["^/vss/?$"];

   vssEndpoint.on_message = [](shared_ptr<WsServer::Connection> connection, shared_ptr<WsServer::Message> message) {
      auto message_str = message->string();
#ifdef DEBUG
      cout << "Server: Message received: \"" << message_str << "\" from " << connection->remote_endpoint_address() << endl;
#endif
      string response = processQuery(message_str, connection->connectionID );
     
      auto send_stream = make_shared<WsServer::SendStream>();
      *send_stream << response;
      connection->send(send_stream);
  };

      vssEndpoint.on_open = [](shared_ptr<WsServer::Connection> connection) {
         connection->connectionID = generateConnID();
         cout << "Server: Opened connection " << connection->remote_endpoint_address()<< "conn ID " << connection->connectionID << endl;
    };

      // See RFC 6455 7.4.1. for status codes
      vssEndpoint.on_close = [](shared_ptr<WsServer::Connection> connection, int status, const string & /*reason*/) {
         UInt32 clientID = connection->connectionID/CLIENT_MASK;
         connections[clientID] = 0;
         removeAllSubscriptions(clientID);
         cout << "Server: Closed connection " << connection->remote_endpoint_address() << " with status code " << status << endl;
    };

  // See http://www.boost.org/doc/libs/1_55_0/doc/html/boost_asio/reference.html, Error Codes for error code meanings
    vssEndpoint.on_error = [](shared_ptr<WsServer::Connection> connection, const SimpleWeb::error_code &ec) {
        UInt32 clientID = connection->connectionID/CLIENT_MASK;
        connections[clientID] = 0;
        removeAllSubscriptions(clientID);
        cout << "Server: Error in connection " << connection->remote_endpoint_address()<<" with con ID "<< connection->connectionID<< ". "
         << "Error: " << ec << ", error message: " << ec.message() << endl;
    };

      cout << "started WS server" << endl; 
      server.start();
}


/**
 * @brief  Test main.
 * @return
 */
int main(int argc, char* argv[])
{

        if(argc == 6) {
           strcpy(PORT , argv[1]);
           strcpy(honoAddress , argv[2]);
           char honoPortStr[16];
           strcpy(honoPortStr , argv[3]);
           honoPort = stoi(honoPortStr, nullptr, 10); 
           strcpy(honoPassword , argv[4]); 
           strcpy(honoDevice , argv[5]);
        } else {
           cerr<<"Usage ./vehicle2cloud <ELM327-PORT> <HONO IP-ADDR> <HONO PORT> <HONO-PASSWORD> <HONO-DEVICE NAME>"<<endl;
           return -1; 
        }

         
        memset(subscribeHandle, 0, sizeof(subscribeHandle));


	//Init new data structure
	initJsonTree();
	initVSS (&mainNode , ptrToSignals);
        
        pthread_t ELMRun_thread;
        pthread_t startWSServer_thread;
        pthread_t honoConnect_thread;

        /* create test run thread which updates the tree */
        if(pthread_create(&ELMRun_thread, NULL, &elmRun, NULL )) {

         cout << "Error creating test run thread"<<endl;
         return 1;

        }

       
        /* create the web socket server thread. */
        if(pthread_create(&startWSServer_thread, NULL, &startWSServer, NULL )) {

         cout << "Error creating websocket server run thread"<<endl;
         return 1;

        }

        /* create the hono connection thread. */
        if(pthread_create(&honoConnect_thread, NULL, &honoConnectRun, NULL )) {

         cout<<"Error creating hono connect run thread"<<endl;
         return 1;

        }
       
      getchar();
}



