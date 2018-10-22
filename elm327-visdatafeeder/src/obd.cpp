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
// sleep in microseconds
extern int AVTHREADSLEEP;
extern int DTCTHREADSLEEP;

extern char PORT[128];
extern int connectionHandle;

// filter out unwanted characters from raw data from the vehicle.
void filter( char * str , int size) {
   int index = 0;
   for(int i=0; i< size; i++) {
        if(str[i] == '\r' || str[i] == '\n')
           continue;
        else if (str[i] == ':') {
           //TODO: this will work only for 1-9 blocks, but this suffices the present requirement. This may cause a problem with Reading DTC, for
           // sensor values should not matter. 
           index = index - 2;
           continue;
        } else if (str[i] == '>') {
           str[index++] = '\0';
           return;
        }
        str[index++] = str[i];
   }
}

void resetELM() {   
   string reset =  "ATZ\r";

   int res = write(connectionHandle,(char*)reset.c_str(), 4);
    
   fsync(connectionHandle);
   usleep(50000);
   
   char read_buffer[64];
   int bytes_read = read(connectionHandle, &read_buffer, 64);

   filter(read_buffer, bytes_read);
   cout << "response for reset is " << string(read_buffer) << endl;
}

void setProtocol(int protocol) {
   // TODO : Needs to be extended for other protocols.
   // set protocol to automatic
   string setProt = "ATSP0\r";
   write(connectionHandle,(char*)setProt.c_str(), 6);
   fsync(connectionHandle);
   usleep(50000);
   char read_buffer[64];
   int bytes_read = read(connectionHandle, &read_buffer, 64);
   filter(read_buffer, bytes_read);
   cout << "response for Setprotocol to automatic is " << string(read_buffer) << endl;
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

   SerialPortSettings.c_cc[VMIN]  = 100; /* Read 10 characters */
   SerialPortSettings.c_cc[VTIME] = 10; // wait for val/10 seconds between each byte received.

   connectionHandle = open(PORT, O_RDWR | O_NOCTTY | O_NDELAY);
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
   
   usleep(200000);
   setProtocol(0);
   return true;
}

string readMode1Data(string command)
{

   char write_buf[6];
   memcpy(write_buf , command.c_str(), 6);

   int res = write(connectionHandle,write_buf, 6);
   fsync(connectionHandle);

   usleep(AVTHREADSLEEP);
   
   char read_buffer[64] = {0};
   int bytes_read = read(connectionHandle, &read_buffer, 64);


   filter(read_buffer, bytes_read);

   string response (read_buffer);
#ifdef DEBUG
   cout << "Sensor Data as string from vehicle ="<< endl << response << endl;
#endif
   
   return response;
}

string readMode3Data() {

   char cmdBuf[3] = {'0','3','\r'};

   int res = write(connectionHandle,cmdBuf, 3);
   fsync(connectionHandle);
   usleep(DTCTHREADSLEEP);
   
   char read_buffer[128] = {0};
   int bytes_read = read(connectionHandle, &read_buffer, 128);

   cout << "Total bytes read =" << bytes_read <<endl;
   
   filter(read_buffer, bytes_read);
   string response (read_buffer);

#ifdef DEBUG
   cout << "Error Data as string from vehicle ="<< endl << response << endl;
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
     filter(response, bytes_read);
     return bytes_read;
}



