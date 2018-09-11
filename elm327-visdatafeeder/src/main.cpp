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

#include "client_wss.hpp"
#include "obd.hpp"
#include"vssMapper.hpp"
#include <json.hpp>

using namespace std;
using namespace jsoncons;

using WssClient = SimpleWeb::SocketClient<SimpleWeb::WSS>;

int connectionHandle = -1;

char PORT[128];
char TOKEN[8096];

string url = "localhost:8090/vss";

shared_ptr<WssClient::Connection> connection = NULL;

void sendRequest(string command) {
   cout << "Send << " << command <<endl;     
   auto send_stream = make_shared<WssClient::SendStream>();
   *send_stream << command;
   connection->send(send_stream);
}

// Thread that updates the tree.
void* elmRun (void* arg) {
   connectOBD(10);
   usleep(1000000);
   // Punp the data into the tree.

   // send Authorize request.
   json authreq;
   authreq["requestId"] = rand() % 99999;
   authreq["action"]= "authorize";
   authreq["tokens"] = string(TOKEN);
   stringstream ss; 
   ss << pretty_print(authreq);
   sendRequest(ss.str());

   usleep(1000000);
    
   
   while(1) {
    // sleep 1 sec
    usleep(1000000);
    if( connection != NULL) {
       string rpm = setRPM();
       cout << " RPM val " << rpm <<endl;
       if( rpm != "Error")
          sendRequest(rpm);
       usleep(1000000);
       string vSpeed = setVehicleSpeed();
       cout << " Speed val " << vSpeed <<endl;
       if( vSpeed != "Error")
          sendRequest(vSpeed);
    } else {
       cout << "No active connection to vis-server at the moment!"<<endl;
    }
  }
}


void* startWSClient(void * arg) {

  WssClient client(url , true ,"Client.pem", "Client.key","CA.pem");

  client.on_message = [](shared_ptr<WssClient::Connection> connection, shared_ptr<WssClient::Message> message) {
    cout << "Response >> " << message->string() << endl;
  };

  client.on_open = [](shared_ptr<WssClient::Connection> conn) {
    cout << "Connection wirh server at " << url << " opened" << endl;
    connection = conn;
    
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


int main(int argc, char* argv[])
{

        if(argc == 3) {
           strcpy(PORT , argv[1]);
           strcpy(TOKEN , argv[2]);
        } else {
           cerr<<"Usage ./elm327_visfeeder <ELM327-PORT>  <JWT TOKEN>"<<endl;
           return -1; 
        }

        
       pthread_t ELMRun_thread;
        /* create test run thread which updates the tree */
        if(pthread_create(&ELMRun_thread, NULL, &elmRun, NULL )) {

         cout << "Error creating test run thread"<<endl;
         return 1;

        }

         usleep(1000000);

        pthread_t startWSClient_thread;

        /* create the web socket client thread. */
        if(pthread_create(&startWSClient_thread, NULL, &startWSClient, NULL )) {

         cout << "Error creating websocket client run thread"<<endl;
         return 1;

        }

   getchar();

}
