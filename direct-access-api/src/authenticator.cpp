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


# include "authenticator.hpp"
#include <iostream>
#include <jsoncons/json.hpp>
#include <iostream>
#include <fstream>

using namespace jsoncons;
using jsoncons::json;


authenticator::authenticator( string secretkey, string algo) {
   algorithm = algo; 
   key = secretkey;

}

string getPublicKey (string fileName) {

  std::ifstream fileStream (fileName);
  std::string key( (std::istreambuf_iterator<char>(fileStream)),
                       (std::istreambuf_iterator<char>()));

  return key;
}

int authenticator::validate (wschannel &channel , string authToken) {
  try {
     auto decoded = jwt::decode(authToken);
     string rsa_pub_key = getPublicKey("jwt.key.pub");
      auto verifier =jwt::verify()
     .allow_algorithm(jwt::algorithm::rs256(rsa_pub_key, "", "", ""));
     verifier.verify(decoded);
     json claims;
     for(auto& e : decoded.get_payload_claims()) {
      //std::cout << e.first << " = " << e.second.to_json() << std::endl;
      std::stringstream ss;
      ss << e.second.to_json();
      claims[e.first] = json::parse(ss.str());
      }

      int ttl = claims["exp"].as<int>();
 
     if (claims.has_key("payload")) {
       json payload = claims["payload"];
       channel.setAuthorized(true);
       channel.setAuthToken(authToken);
       channel.accesses = payload;
     }

    return ttl;
  } catch (const exception &e) {
     return -1;
  }
}

bool authenticator::isStillValid (wschannel &channel) {

  string token = channel.getAuthToken();
  int ret = validate (channel , token);
  
   if( ret == -1) {
      return false;
   } else {
      return true;
   }
}
