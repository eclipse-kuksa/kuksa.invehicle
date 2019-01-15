/*
 * ******************************************************************************
 * Copyright (c) 2018 Robert Bosch GmbH.
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
#include "Simple-WebSocket-Server/server_wss.hpp"
#include "directAccessProcessor.hpp"
#include "authenticator.hpp"
#include "obeclient.hpp"
#include "vcanhandler.hpp"

using namespace std;

#ifndef __WSSERVER_H__
#define __WSSERVER_H__

using WssServer = SimpleWeb::SocketServer<SimpleWeb::WSS>;
using WsServer = SimpleWeb::SocketServer<SimpleWeb::WS>;

class wsserver {
 private:
  WssServer* secureServer;
  WsServer* insecureServer;
  bool isSecure;

 public:
  class directAccessProcessor* cmdProcessor;
  class authenticator* tokenValidator;

  wsserver(int port, bool secure);
  ~wsserver();
  void startServer(string endpointName);
  void sendToConnection(uint32_t connID, string message);
};
#endif
