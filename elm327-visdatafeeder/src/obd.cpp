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
#include"obd.hpp"
#include <iostream>
#include <fcntl.h>
#include <termios.h>
#include <unistd.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

using namespace std;

#define BAUD_RATE B38400

int first = 0;

extern char* PORT;
extern int connectionHandle;

void removeSlashRN( char * str) {

   // replace carriage return and new line with empty string.
   for(int i=0; i< sizeof(str); i++) {
        if(str[i] == '\r' || str[i] == '\n')
           str[i] = ' ';

   }

}

void resetELM() {   
   string reset =  "ATZ\r";

   int res = write(connectionHandle,(char*)reset.c_str(), 4);
    
   fsync(connectionHandle);
   usleep(500000);
   
   char read_buffer[64];
   int bytes_read = read(connectionHandle, &read_buffer, 64);

   removeSlashRN(read_buffer);
   cout << "response for reset is " << string(read_buffer) << endl;
}

void setProtocol(int protocol) {
   // set protocol to automatic
   string setProt = "ATSP0\r";
   write(connectionHandle,(char*)setProt.c_str(), 6);
   fsync(connectionHandle);
   usleep(500000);
   char read_buffer[64];
   int bytes_read = read(connectionHandle, &read_buffer, 64);
   removeSlashRN(read_buffer);
   cout << "resp for ATSP0 is " << string(read_buffer) << endl;
}

bool connectOBD(int timeout)
{

   if( connectionHandle != -1 ) {
       cout<<"seems like a connection is already active !!"<<endl;
       return false;
   }

   struct termios SerialPortSettings;
   memset(&SerialPortSettings, 0, sizeof(SerialPortSettings));
   
   // get the comm parameters.
   tcgetattr(connectionHandle, &SerialPortSettings);
   
    SerialPortSettings.c_iflag &= ~(INLCR | ICRNL);
    SerialPortSettings.c_iflag |= IGNPAR | IGNBRK;
    SerialPortSettings.c_oflag &= ~(OPOST | ONLCR | OCRNL);
    SerialPortSettings.c_cflag &= ~(PARENB | PARODD | CSTOPB | CSIZE | CRTSCTS); /* do not enable flow control, disable parity checking */
    SerialPortSettings.c_cflag |= CLOCAL | CREAD | CS8;
    SerialPortSettings.c_lflag &= ~(ICANON | ISIG | ECHO);

   SerialPortSettings.c_cc[VMIN]  = 10; /* Read 10 characters */
   SerialPortSettings.c_cc[VTIME] = 10; // wait for val/10 seconds between each byte received.

   connectionHandle = open("/dev/rfcomm0", O_RDWR | O_NOCTTY | O_NDELAY);
   // set the comm parameters for ELM 327 with Bluetooth.
   cfsetispeed(&SerialPortSettings,BAUD_RATE);
   cfsetospeed(&SerialPortSettings,BAUD_RATE);

   if(connectionHandle == -1) {
      cout<< " Error while opening the serial port connection to ELM 327" << endl;
      return false;
   }
   else {
      cout<< " Connection to the port sucessful with val "<< connectionHandle << endl;
   }
 
   tcsetattr(connectionHandle,TCSANOW,&SerialPortSettings);

   // Apply ELM 327 settings.
   fcntl(connectionHandle, F_SETFL, 0);

   resetELM();
   
   usleep(1000000);
      
   setProtocol(0);

   return true;
}

string readMode1Data(string command)
{

   char write_buf[6];
   memcpy(write_buf , command.c_str(), 6);

   int res = write(connectionHandle,write_buf, 6);
   fsync(connectionHandle);

   usleep(500000);
   
   char read_buffer[64] = {0};
   int bytes_read = read(connectionHandle, &read_buffer, 64);
  
   removeSlashRN(read_buffer);

   string response (read_buffer);
#ifdef DEBUG
   cout << "Data as string from vehicle ="<< endl << response << endl;
#endif
   
   return response;
}


void closeConnection() {
    close(connectionHandle);
}


int testCommands(string command, char* response) {
     
     command = command + '\r';
     int res = write(connectionHandle,(char*)command.c_str(), command.length());
     fsync(connectionHandle);

     usleep(500000);

#ifdef DEBUG
     if( res != length) {
        cout<< "not all request bytes written to the buffer! bytes written = " << res << endl;
     }
#endif
     int bytes_read = read(connectionHandle, response, 256);

#ifdef DEBUG
     cout << "Total bytes read as response = " << bytes_read << endl;
#endif
     removeSlashRN(response);
     return bytes_read;
}



