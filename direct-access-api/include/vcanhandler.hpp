/*
 * ******************************************************************************
 * Copyright (c) 2019 KocSistem Bilgi ve Iletisim Hizmetleri A.S..
 *
 * All rights reserved. This program and the accompanying materials
 * are made available under the terms of the Eclipse Public License v2.0
 * which accompanies this distribution, and is available at
 * https://www.eclipse.org/org/documents/epl-2.0/index.php
 *
 *  Contributors:
 *      Initial functionality - Ismail Burak Oksuzoglu, Erdem Ergen, Aslihan Cura (KocSistem Bilgi ve Iletisim Hizmetleri A.S.) 
 * *****************************************************************************
 */

#ifndef VCANHANDLER_H
#define VCANHANDLER_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>
#include <stdint.h>
#include <sstream>
#include <cstdio>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <array>
#include <unistd.h>
#include <net/if.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <thread>
#include <linux/can.h>
#include <linux/can/raw.h>
#include "common.hpp"
#include "dbmanager.hpp"
#include "obeclient.hpp"

#define MAX_RAND_TRY_LIMIT 10
#define MIN_VCAN_NO 0
#define VCAN_NO_RANGE 100
#define BUFFER_SIZE 100

using namespace std;

class vcanhandler {
 private:
  string generateVcanName();

 public:
  vcanhandler();
  ~vcanhandler();
  string createVcan();
  string createVcan(string vcan);
  bool vcanExists(string vcan);
  void deleteAllVcan(int range);
  void deleteVcan(string vcan);

  void vcan_read(string vcan_name);
  void start_vcan_listener(string vcan_name);
  void start_all_listeners();
};

class vcanlistener {
 private:
  int can_sock;

 public:
  string vcan_name;
  vcanlistener(string _vcan_name);
  ~vcanlistener();
  void vcan_read(string vcan_name);
  e_result vcan_socket_init();
  void vcan_write_frame(struct can_frame* frame);
};

#endif  // VCANHANDLER_H
