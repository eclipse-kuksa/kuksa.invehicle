#include "honoMqtt.hpp"

using namespace std;


/**
 * A callback class for use with the main MQTT client.
 */
class callback : public virtual mqtt::callback, public virtual mqtt::iaction_listener 
{
public:
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
		std::cout << "Message arrived" << std::endl;
		std::cout << "\ttopic: '" << msg->get_topic() << "'" << std::endl;
		std::cout << "\tpayload: '" << msg->to_string() << "'\n" << std::endl;
        }

        void on_failure(const mqtt::token& tok) override {
		if (tok.get_message_id() != 0)
			std::cout << " for token: [" << tok.get_message_id() << "]" << std::endl;
		std::cout << std::endl;
	}

	void on_success(const mqtt::token& tok) override {
		if (tok.get_message_id() != 0)
			std::cout << " for token: [" << tok.get_message_id() << "]" << std::endl;
		auto top = tok.get_topics();
		if (top && !top->empty())
			std::cout << "\ttoken topic: '" << (*top)[0] << "', ..." << std::endl;
		std::cout << std::endl;
	}
};

/**
 * A base action listener.
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

/////////////////////////////////////////////////////////////////////////////


  
void HonoMqtt::connect (string honoAddr , string clientID) {

   p_Client = new mqtt::async_client (honoAddr, clientID);
   callback cb;
   p_Client->set_callback(cb);
   mqtt::connect_options connOpts;
   connOpts.set_keep_alive_interval(20);
   connOpts.set_clean_session(true);

   try {
         cout << "\nConnecting..." << endl;
         mqtt::token_ptr conntok = p_Client->connect(connOpts);
	 cout << "Waiting for the connection..." << endl;
	 conntok->wait();
         cout << "  ...OK" << endl;
   } catch (const mqtt::exception& exc) {
		cerr << exc.what() << endl;
		throw exc;
   }
}

void HonoMqtt::subscribe(string topic) {
   
   callback subListener;
   p_Client->subscribe(topic, 0, nullptr, subListener);
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
