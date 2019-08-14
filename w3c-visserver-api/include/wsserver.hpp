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

#ifndef __WSSERVER_H__
#define __WSSERVER_H__

#include "server_wss.hpp"

class vsscommandprocessor;
class vsscommandprocessor;
class subscriptionhandler;
class authenticator;
class vssdatabase;
class accesschecker;

class wsserver {
 private:
  SimpleWeb::SocketServer<SimpleWeb::WSS> *secureServer;
  SimpleWeb::SocketServer<SimpleWeb::WS> *insecureServer;
  bool isSecure;

 public:
  vsscommandprocessor* cmdProcessor;
  subscriptionhandler* subHandler;
  authenticator* tokenValidator;
  vssdatabase* database;
  accesschecker* accessCheck;

  wsserver(int port, bool secure);
  ~wsserver();
  void startServer(std::string endpointName);
  void sendToConnection(uint32_t connID, std::string message);
  void start();
};
#endif
