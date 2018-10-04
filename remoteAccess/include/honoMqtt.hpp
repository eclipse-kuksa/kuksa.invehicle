#include <iostream>
#include <cstdlib>
#include <string>
#include <thread>	// For sleep
#include <atomic>
#include <chrono>
#include <cstring>
#include "mqtt/async_client.h"


using namespace std;


class HonoMqtt {

private: 
    mqtt::async_client* p_Client;

public:
   void connect (string honoAddr , string clientID);
   void subscribe(string topic);
   void publish (string topic, string data);
   void disconnect();
};
