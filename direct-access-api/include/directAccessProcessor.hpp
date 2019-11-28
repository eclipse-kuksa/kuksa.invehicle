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
#ifndef __VSSCOMMANDPROCESSOR_H__
#define __VSSCOMMANDPROCESSOR_H__

#include <string>
#include "wschannel.hpp"
#include "accesschecker.hpp"
#include <jsoncons/json.hpp>
#include "vcanhandler.hpp"
#include "dbmanager.hpp"

#define PERM_MNGT_BUFFER_SIZE 1000

using namespace std;
using namespace jsoncons;
using jsoncons::json;


class directAccessProcessor {
 private:
  string ks_token;
  string perm_mngt_srv_address = "/home/a02482333/repo/permission-mngt/socket";
  class authenticator* tokenValidator = NULL;
  class accesschecker* accessValidator = NULL;
  class vcanhandler* vcanHandler = NULL;

  string processCreate(json perm_json, string rchannel);
  string processDelete(string vchannel);

 public:
  directAccessProcessor(class authenticator* vdator);
  string processQuery(string req_json, class wschannel& channel);
};

#endif
