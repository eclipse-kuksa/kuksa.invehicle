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
#include <iostream>
#include <cstdlib>
#include <string>
#include <thread>	// For sleep
#include <atomic>
#include <chrono>
#include <cstring>
#include "mqtt/async_client.h"


using namespace std;


class HonoMqtt : public virtual mqtt::callback, public virtual mqtt::iaction_listener {

private: 
    
    mqtt::async_client* p_Client;

public:
   
   void connect (string honoAddr , string clientID, string userName, string password);
   void publish (string topic, string data);
   void disconnect();

   void connection_lost(const string& cause) override {
		cout << "\nConnection lost" << endl;
		if (!cause.empty())
			cout << "\tcause: " << cause << endl;
   }

   void delivery_complete(mqtt::delivery_token_ptr tok) override {
		cout << "\tDelivery complete for token: "
			<< (tok ? tok->get_message_id() : -1) << endl;
   }

   void message_arrived(mqtt::const_message_ptr msg) override {
		/*std::cout << "Message arrived" << std::endl;
		std::cout << "\ttopic: '" << msg->get_topic() << "'" << std::endl;
		std::cout << "\tpayload: '" << msg->to_string() << "'\n" << std::endl;*/
                (*onMsg)(msg->to_string());
   }

   void on_failure(const mqtt::token& tok) override {
		if (tok.get_message_id() != 0)
			std::cout << " for token: [" << tok.get_message_id() << "]" << std::endl;
		std::cout << std::endl;
   }

   void on_success(const mqtt::token& tok) override {
		cout << "connection successful "<<endl;
   }
};
