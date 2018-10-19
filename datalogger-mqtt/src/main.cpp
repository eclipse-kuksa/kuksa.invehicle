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

// delay between sending each signals in microseconds
#define SENDDELAY 50000

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


const std::string CLIENT_ID { "datalogger-mqtt" };

const string PUB_TOPIC {"telemetry"};
string fullTopic;

const int QOS = 0;

const auto TIMEOUT = std::chrono::seconds(10);

class HonoMqtt* honoConn;

// callback method for receiving messages from hono.
void onMessageFromHono(string message) {

   cout <<" Message arrived in main " << message <<endl;

}

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
  
    if( !root.has_key("value")) {
        cout << " No value from server found" <<endl;
        return;
    } else if ( root["value"].as<string>() == "---") {
        cout << " No value set !! server has returned --- for"<< root["path"].as<string>() <<endl;
        return;
    }    

    if( !root.has_key("value")) {
        cout << " No value returned from server"<< endl;
        return;
    } 


    std::string value = root["value"].as<string>();
       
    int reqID = root["requestId"].as<int>();
    string signal;
    json valJson;
    if(reqID == 1234) {
       signal = "RPM";
       int val = stoi(value, nullptr, 10);
       valJson[signal] = val;
    } else if (reqID == 1235) {
       signal = "SPEED";
       int val = stoi(value, nullptr, 10);
       valJson[signal] = val;
    } else if (reqID == 1236) {
       signal = "ERROR";
       int val = 0;
       if(value == "true")
           val = 1;
       valJson[signal] = val;      
    } else if (reqID == 1237) {
       signal = "ERROR2";
       int val = 0;
       if(value == "true")
           val = 1;
       valJson[signal] = val;      
    } else if (reqID == 1238) {
       signal = "ERROR3";
       int val = 0;
       if(value == "true")
           val = 1;
       valJson[signal] = val;      
    } else if (reqID == 1239) {
       signal = "FUEL";
       int val = stoi(value, nullptr, 10);
       valJson[signal] = val;
    }
    honoConn->publish(PUB_TOPIC, valJson.as<string>());
}


void* sendSensorValues (void* arg) {

  if(honoConnect) {
  usleep(SENDDELAY);
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
      cout << honoAddr << endl;
      string userName = string(honoDevice) + "@DEFAULT_TENANT";
      string password(honoPassword);
      honoConn->connect(honoAddr, CLIENT_ID, userName, password);
      honoConn->setMessageCB(onMessageFromHono);
   } catch ( mqtt::exception& e) {

   }

  // send data to hono instance.
  while(1) {
   string rpm_req = "{\"action\": \"get\", \"path\": \"Signal.OBD.RPM\", \"requestId\": 1234 }";

    
    *send_stream << rpm_req;
    connection->send(send_stream);    


    usleep(SENDDELAY);  
    string vSpeed_req = "{\"action\": \"get\", \"path\": \"Signal.OBD.Speed\", \"requestId\": 1235 }";
    
    *send_stream << vSpeed_req;
    connection->send(send_stream); 

    
    usleep(SENDDELAY);

   string dtc2_req = "{\"action\": \"get\", \"path\": \"Signal.OBD.DTC2\", \"requestId\": 1236 }";
    
    *send_stream << dtc2_req;
    connection->send(send_stream);

    usleep(SENDDELAY); 

    string dtc3_req = "{\"action\": \"get\", \"path\": \"Signal.OBD.DTC3\", \"requestId\": 1237 }";
    
    *send_stream << dtc3_req;
    connection->send(send_stream);

    usleep(SENDDELAY); 

    string dtc4_req = "{\"action\": \"get\", \"path\": \"Signal.OBD.DTC4\", \"requestId\": 1238 }";
    
    *send_stream << dtc4_req;
    connection->send(send_stream);

    usleep(SENDDELAY); 

    string fuel_req = "{\"action\": \"get\", \"path\": \"Signal.OBD.FuelLevel\", \"requestId\": 1239 }";
    
    *send_stream << fuel_req;
    connection->send(send_stream);

    usleep(SENDDELAY); 
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
        /* create the sensor values thread. */
        if(pthread_create(&honoConnect_thread, NULL, &sendSensorValues, NULL )) {

         cout<<"Error creating send sensor values thread"<<endl;
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

        fullTopic = PUB_TOPIC +"/"+"DEFAULT_TENANT/"+string(honoDevice);
        cout << "Complete topic for hono mqtt is " << fullTopic << endl;
        
       
     pthread_t startWSClient_thread;

        /* create the web socket client thread. */
        if(pthread_create(&startWSClient_thread, NULL, &startWSClient, NULL )) {

         cout << "Error creating websocket client run thread"<<endl;
         return 1;

        }
while (1) { usleep (1000000); };
}



