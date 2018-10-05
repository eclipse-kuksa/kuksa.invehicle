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
#include "honoMqtt.hpp"

using namespace std;


/**
 * A base action listener for pub.
 */
class action_listener_pub : public virtual mqtt::iaction_listener
{
protected:
	void on_failure(const mqtt::token& tok) override {
		cout << "\tListener failure for token: "
			<< tok.get_message_id() << endl;
	}

	void on_success(const mqtt::token& tok) override {
		cout << "\tListener success for token: "
			<< tok.get_message_id() << endl;
	}
};

/**
 * A base action listener for pub.
 */
class action_listener_sub : public virtual mqtt::iaction_listener
{
protected:
	void on_failure(const mqtt::token& tok) override {
		cout << "\tListener failure for token: "
			<< tok.get_message_id() << endl;
	}

	void on_success(const mqtt::token& tok) override {
		cout << "\tListener success for token: "
			<< tok.get_message_id() << endl;
	}
};

/////////////////////////////////////////////////////////////////////////////


  
void HonoMqtt::connect (string honoAddr , string clientID, string userName, string password) {

   p_Client = new mqtt::async_client (honoAddr, clientID);
   p_Client->set_callback(*this);
   mqtt::connect_options connOpts;
   connOpts.set_keep_alive_interval(20);
   connOpts.set_clean_session(true);
   connOpts.set_user_name(userName);
   connOpts.set_password(password);

   try {
         cout << "\nConnecting..." << endl;
         mqtt::token_ptr conntok = p_Client->connect(connOpts, nullptr, *this);
	 cout << "Waiting for the connection..." << endl;
	 conntok->wait();
         cout << "  ...OK" << endl;
   } catch (const mqtt::exception& exc) {
		cerr << exc.what() << endl;
		throw exc;
   }
}

void HonoMqtt::subscribe(string topic) {
   
   
   p_Client->subscribe(topic, 0, nullptr, *this);
}
   
void HonoMqtt::publish (string topic, string data) {
    cout << "\nSending next message..." << endl;
    action_listener_pub listener;
    mqtt::message_ptr pubmsg = mqtt::make_message(topic, "Test");
    mqtt::delivery_token_ptr pubtok;
    pubtok = p_Client->publish(pubmsg, nullptr, listener);
    pubtok->wait();
    cout << "  ...OK" << endl;
    
}

void HonoMqtt::disconnect() {
   // Disconnect
   cout << "\nDisconnecting..." << endl;
   mqtt::token_ptr  conntok = p_Client->disconnect();
   conntok->wait();
   cout << "  ...OK" << endl;
}

void HonoMqtt::setMessageCB(void(*msgCB)(string)) {
   onMsg = msgCB;
}







