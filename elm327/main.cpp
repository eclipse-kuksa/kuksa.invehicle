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
#include "obd.hpp"

char* PORT;
int connectionHandle;
using namespace std;


int main(int argc, char* argv[])
{
     string command;
     char response[256] = {'\0'};;
        if(argc == 2) {
          PORT = argv[1];
          cout <<" ELM 327 app started with PORT= " << PORT <<endl; 
        } else {
          cerr <<"Usage ./elm327 <PORT>" <<endl;
        }

      
       while(true) {
         cout<<"ENTER COMMAND:" << endl;
         getline (cin, command);
         testCommands(command, response);
         cout<<"RESPONSE:"<< endl<< response <<endl;
       }
       
      getchar();
      return 0;
}

