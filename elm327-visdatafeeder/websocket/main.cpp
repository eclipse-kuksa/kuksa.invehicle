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

#include <json.hpp>
#include "actuatorTest.hpp"
#include "client_wss.hpp"
#include "obd.hpp"
#include "vssMapper.hpp"

using namespace std;
using namespace jsoncons;

using WssClient = SimpleWeb::SocketClient<SimpleWeb::WSS>;

// Websocket connection mutex.
pthread_mutex_t wsMutex;

// Websocket connection status flag. Initially false.
bool isClosed = false;

// Cmd line parameters
char PORT[128];
char TOKEN[8096];
int AVTHREADSLEEP;
int DTCTHREADSLEEP;

string url = "localhost:8090/vss";

// Websocket handle.
shared_ptr<WssClient::Connection> connection = NULL;

void sendRequest(string command) {
  cout << "Send << " << command << endl;
  auto send_stream = make_shared<WssClient::SendStream>();
  *send_stream << command;
  pthread_mutex_lock(&wsMutex);
  connection->send(send_stream);
  pthread_mutex_unlock(&wsMutex);
}

// Thread that updates AVs on the tree.
void* elmActualValuesRun(void* arg) {
  connectOBD(10);
  // Sleep 100ms.
  usleep(100000);
  // Punp the data into the tree.

  // send Authorize request.
  json authreq;
  authreq["requestId"] = rand() % 99999;
  authreq["action"] = "authorize";
  authreq["tokens"] = string(TOKEN);
  stringstream ss;
  ss << pretty_print(authreq);
  sendRequest(ss.str());

  // Sleep 100ms.
  usleep(100000);

  // subsribe to throttle topic.
  json subscibeReq;
  subscibeReq["requestId"] = rand() % 99999;
  subscibeReq["action"] = "subscribe";
  subscibeReq["path"] =
      "Vehicle.Drivetrain.InternalCombustionEngine.ThrottleTest";
  stringstream sstream;
  sstream << pretty_print(subscibeReq);
  sendRequest(sstream.str());

  int count = 0;
  while (1) {
    if (connection != NULL) {
      // Sleep between values. Configurable as cmd line argument.
      usleep(AVTHREADSLEEP);
      string rpm = setRPM();
#ifdef DEBUG
      cout << " RPM val " << rpm << endl;
#endif
      if (rpm != "Error") sendRequest(rpm);
      string vSpeed = setVehicleSpeed();
#ifdef DEBUG
      cout << " Speed val " << vSpeed << endl;
#endif
      if (vSpeed != "Error") sendRequest(vSpeed);
      // Fuel status is updated leisurely.
      if (count > 200) {
        string fuel = setFuelLevel();
#ifdef DEBUG
        cout << " Fuel val " << rpm << endl;
#endif
        if (fuel != "Error") sendRequest(fuel);
      }  // Fuel update end
    } else {
      cout << "No active connection to vis-server at the moment!" << endl;
    }
    count++;
  }
  cout << "Exited the elm AVs update thread" << endl;
}

// Thread that updates the Errors ( DTCs)
void* elmDTCRun(void* arg) {
  // Do nothing for the first 10 second.
  usleep(10000000);

  while (1) {
    if (connection != NULL) {
      list<string> errors = readErrors();

      int size = errors.size();

      if (size > 0) {
        for (string err : errors) {
          sendRequest(err);
#ifdef DEBUG
          cout << err << endl;
#endif
        }
      }

    } else {
      cout << "No active connection to vis-server at the moment!" << endl;
    }
    // Sleep between reading DTC. Configurable as cmd line argument.
    usleep(DTCTHREADSLEEP);
  }
  cout << "Exited the elm DTC update thread" << endl;
}

// on messages received.
void onMessage(string message) {
#ifdef DEBUG
  cout << "Response >> " << message << endl;
#endif
  json msg;
  msg = json::parse(message);

  if (!msg.has_key("value")) {
    return;
  } else if (msg.has_key("subscriptionId")) {
    int percent = msg["value"].as<int>();
    moveThrottleValve(percent);
  }
}

void* startWSClient(void* arg) {
  WssClient client(url, true, "Client.pem", "Client.key", "CA.pem");

  client.on_message = [](shared_ptr<WssClient::Connection> connection,
                         shared_ptr<WssClient::Message> message) {
    onMessage(message->string());
  };

  client.on_open = [](shared_ptr<WssClient::Connection> conn) {
    cout << "Connection with server at " << url << " opened" << endl;
    connection = conn;
    pthread_t ELMAVRun_thread;
    /* create test run thread which updates the tree */
    if (pthread_create(&ELMAVRun_thread, NULL, &elmActualValuesRun, NULL)) {
      cout << "Error creating AVs update thread" << endl;
      return 1;
    }

    pthread_t ELMDTCRun_thread;
    /* create test run thread which updates the tree */
    if (pthread_create(&ELMDTCRun_thread, NULL, &elmDTCRun, NULL)) {
      cout << "Error creating DTC check thread" << endl;
      return 1;
    }

  };

  client.on_close = [](shared_ptr<WssClient::Connection> /*connection*/,
                       int status, const string& /*reason*/) {
    cout << "Connection closed with status code " << status << endl;
    connection = NULL;
    isClosed = true;
  };

  // See
  // http://www.boost.org/doc/libs/1_55_0/doc/html/boost_asio/reference.html,
  // Error Codes for error code meanings
  client.on_error = [](shared_ptr<WssClient::Connection> /*connection*/,
                       const SimpleWeb::error_code& ec) {
    cout << "Error: " << ec << ", message: " << ec.message() << endl;
    isClosed = true;
  };

  client.start();
}

// Main
int main(int argc, char* argv[]) {
  if (argc == 5) {
    strcpy(PORT, argv[1]);
    strcpy(TOKEN, argv[2]);
    AVTHREADSLEEP = atoi(argv[3]);
    DTCTHREADSLEEP = atoi(argv[4]);
  } else {
    cerr << "Usage ./elm327_visfeeder <ELM327-PORT>  <JWT TOKEN> "
            "<AVTHREADDELAY> <DTCTHREADDELAY>"
         << endl;
    return -1;
  }

  pthread_t startWSClient_thread;

  /* create the web socket client thread. */
  if (pthread_create(&startWSClient_thread, NULL, &startWSClient, NULL)) {
    cout << "Error creating websocket client run thread" << endl;
    return 1;
  }

  while (!isClosed) {
    usleep(1000000);
  };  // Loop until websocket connection exists.
  cout << "Exiting ELM327-datafeeder main thread because of possible error"
       << endl;
  return 1;
}
