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
#include "emailHTTP.hpp"
#include <json.hpp>

#define MAX_ERRORS 10

#define USER_EMAIL_FILE "/tmp/email"


using namespace std;

using WssClient = SimpleWeb::SocketClient<SimpleWeb::WSS>;
using namespace jsoncons;
using jsoncons::json;

bool mailsent[MAX_ERRORS];

string emailID ="";

char emailServerAddress[256];
char emailServerPort[64];

char TOKEN[2048];

const string DEFAULT_TENANT = "DEFAULT_TENANT";

std::string query;

string url = "localhost:8090/vss";

shared_ptr<WssClient::Connection> connection = NULL;


string readEmailAddr() {

    std::ifstream ifs (USER_EMAIL_FILE, std::ifstream::in);
    
   if( !ifs.is_open()) {
       cout << "User E-Mail iD not configured!!" << endl;
       return ""; 
   }
 

    string email;
    getline (ifs,email);
    ifs.close();
    cout <<"User Email= " << email << endl;
    return email;

}


void sendEmailToOwner( string resp) {


   string emailAddr =  readEmailAddr();
  
   if(emailID != emailAddr) {
      cout << "Email Address changed to " << emailAddr << endl;
      for( int i = 0; i<MAX_ERRORS ; i++) {
          mailsent[i] = false;
      } 
      emailID = emailAddr;
      
   }

   if( emailID == "") {
      cout << "Configure E-mail Address of the User. This app is useless without it!" << endl;
      return;
   }

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
    
    if((reqID > -1 && reqID < MAX_ERRORS) && value == "true") {
       
      if(!mailsent[reqID]) {
         int status = sendEmail(emailID, "Error Found In your Car!" , "Hello Sir, An Error has been found in your car, Please contact your nearest service station. Error details = P010" + std::to_string(reqID));
         if ( status == 1) {
             cout << " Email sent to user successfully!" << endl;
             mailsent[reqID] = true;
         } else {
             cout << " Error occured while trying to send email to owner" << endl;
         }
      }
       
    }
}


void* visConnectRun (void* arg) {

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


  // send data to hono instance.
  while(1) {
    
    string dtc_1 = "{\"action\": \"get\", \"path\": \"Signal.OBD.DTC1\", \"requestId\": 5 }";

    
    *send_stream << dtc_1;
    connection->send(send_stream);    



     // sleep 0.2 sec
    usleep(200000);  
    string dtc_2 = "{\"action\": \"get\", \"path\": \"Signal.OBD.DTC2\", \"requestId\": 6 }";
    
    *send_stream << dtc_2;
    connection->send(send_stream); 


    usleep(200000);  
    string dtc_3 = "{\"action\": \"get\", \"path\": \"Signal.OBD.DTC3\", \"requestId\": 7 }";
    
    *send_stream << dtc_3;
    connection->send(send_stream); 

    
    
     // sleep 2 sec
    usleep(2000000);
  }
}

void* startWSClient(void * arg) {

  WssClient client(url , true, "Client.pem", "Client.key", "CA.pem");

  client.on_message = [](shared_ptr<WssClient::Connection> connection, shared_ptr<WssClient::Message> message) {
    sendEmailToOwner(message->string());
  };

  client.on_open = [](shared_ptr<WssClient::Connection> conn) {
    cout << "Connection with server at " << url << " opened" << endl;
    connection = conn;
       pthread_t visConnect_thread;
        /* create the hono connection thread. */
        if(pthread_create(&visConnect_thread, NULL, &visConnectRun, NULL )) {

         cout<<"Error creating VIS server connect run thread"<<endl;
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

        if(argc == 4) {
           strcpy(emailServerAddress , argv[1]);
           strcpy(emailServerPort , argv[2]);
           strcpy(TOKEN, argv[3]);
        } else {
           cerr<<"Usage ./emailnotify <EMAIL-SERVER-IP> <EMAIL-SERVER-PORT> <JWT TOKEN>"<<endl;
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



