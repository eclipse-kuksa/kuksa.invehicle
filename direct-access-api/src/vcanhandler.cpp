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

#include "vcanhandler.hpp"

vcanhandler::vcanhandler() {}
vcanhandler::~vcanhandler() {}

bool vcanhandler::vcanExists(string vcan) {
  array<char, 128> buffer;
  string result;
  int lcount = 0;

  string ipstr = "ip link|grep " + vcan + ":";
  shared_ptr<FILE> pipe(popen(ipstr.c_str(), "r"), pclose);
  if (!pipe) throw std::runtime_error("popen() failed!");

  while (!feof(pipe.get())) {
    lcount++;
    if (fgets(buffer.data(), 128, pipe.get()) != nullptr)
      result += buffer.data();
  }

  if (lcount > 1) {
    return true;
  } else {
    return false;
  }
}

string vcanhandler::generateVcanName() {
  int max = 0;
  string vcan;

  while (max < MAX_RAND_TRY_LIMIT) {
    max++;
    vcan = "vcan" + to_string(MIN_VCAN_NO + rand() % VCAN_NO_RANGE);

    // check if already exists
    if (vcanExists(vcan) == false) return vcan;
  }
  return "";
}

void vcanhandler::deleteVcan(string vcan) {
  string vcan_delete = "ip link delete " + vcan;
  system(vcan_delete.c_str());
  cout << vcan << " ip link deleted" << endl;
}

void vcanhandler::deleteAllVcan(int range) {
  int i = 0;
  while (i <= range) {
    deleteVcan("vcan" + to_string(i));
    i++;
  }
}

string vcanhandler::createVcan() {
  array<char, 128> buffer;
  string result, vcan_add, vcan_state_up;
  int lcount = 0;

  // generate a valid random vcan name
  string vcan = generateVcanName();

  if (vcan.length() == 0) {
    cout << "failed to generate vcan name" << endl;
    return "-1";
  }

  // add & set up vcan
  vcan_add = "ip link add dev " + vcan + " type vcan";
  vcan_state_up = "ip link set up " + vcan;

  shared_ptr<FILE> pipe(popen(vcan_add.c_str(), "r"), pclose);
  if (!pipe) throw std::runtime_error("popen() failed!");

  while (!feof(pipe.get())) {
    lcount++;
    if (fgets(buffer.data(), 128, pipe.get()) != nullptr)
      result += buffer.data();
  }

  if (lcount <= 1) {
    system(vcan_state_up.c_str());
    cout << vcan << " created." << endl;

    return vcan;
  } else {
    cout << "[" << result << "] " << vcan << " creation failed." << endl;
    return "-1";
  }
}

string vcanhandler::createVcan(string vcan) {
  array<char, 128> buffer;
  string result, vcan_add, vcan_state_up;
  int lcount = 0;

  // add & set up vcan
  vcan_add = "ip link add dev " + vcan + " type vcan";
  vcan_state_up = "ip link set up " + vcan;

  shared_ptr<FILE> pipe(popen(vcan_add.c_str(), "r"), pclose);
  if (!pipe) throw std::runtime_error("popen() failed!");

  while (!feof(pipe.get())) {
    lcount++;
    if (fgets(buffer.data(), 128, pipe.get()) != nullptr)
      result += buffer.data();
  }

  if (lcount <= 1) {
    system(vcan_state_up.c_str());
    cout << vcan << " created." << endl;

    return vcan;
  } else {
    cout << "[" << result << "] " << vcan << " creation failed." << endl;
    return "-1";
  }
}

e_result vcanlistener::vcan_socket_init() {
  struct sockaddr_can addr;
  struct ifreq ifr;

  const char *ifname = vcan_name.c_str();

  if ((can_sock = socket(PF_CAN, SOCK_RAW, CAN_RAW)) < 0) {
    perror("Error while opening vcan socket");
    return FAILURE;
  }

  strcpy(ifr.ifr_name, ifname);
  ioctl(can_sock, SIOCGIFINDEX, &ifr);

  addr.can_family = AF_CAN;
  addr.can_ifindex = ifr.ifr_ifindex;

  printf("%s at index %d\n", ifname, ifr.ifr_ifindex);

  if (bind(can_sock, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
    perror("Error in vcan socket bind");
    return FAILURE;
  }

  return SUCCESS;
}

void vcanlistener::vcan_read(string vcan_name) {
  dbmanager db;
  cout << "Starting to listen vcan bus: " << vcan_name << endl;
  struct can_frame frame;
  char can_msg[BUFFER_SIZE] = {};
  bool check = false;

  while (1) {
    if (read(can_sock, &frame, sizeof(struct can_frame)) < 0)
      printf("Failed to read to vcan bus\n");
    else {
      // if id in write rules, send to obe
      check = false;
      vector<int> write_rules = db.get_write_rules(vcan_name);
      for (int w : write_rules) {
        if ((frame.can_id & 0x1FFFFFFF) == w) {
          check = true;
          break;
        }
      }

      if (check == true) {
        // send to obe
        std::cout << "send to obe" << endl;

        prepare_outgoing_msg(can_msg, &frame);

        if (write(sockfd, &can_msg, BUFFER_SIZE) < 0)
          printf("Failed to send msg to daa_obe\n");
        else
          printf("%s -> frame sent to daa_obe\n", can_msg);

      } else {
        std::cout << "no write permissions" << endl;
      }

      memset(&can_msg, '\0', sizeof(can_msg));
    }
  }
}

void vcanlistener::vcan_write_frame(struct can_frame *frame) {
  if (write(can_sock, frame, sizeof(struct can_frame)) < 0)
    printf("Failed to write to vcan bus\n");
  else
    printf("Frame sent to vcan bus\n");
}

vcanlistener::vcanlistener(string _vcan_name) { vcan_name = _vcan_name; }
vcanlistener::~vcanlistener() {}

void vcanhandler::start_vcan_listener(string vcan_name) {
  vcanlistener listener(vcan_name);

  if (listener.vcan_socket_init() == SUCCESS) {
    thread vcan_thread(&vcanlistener::vcan_read, listener, listener.vcan_name);
    vcan_thread.detach();
  } else {
    cout << "Failed to connect to virtual can bus: " << vcan_name << endl;
  }
}

void vcanhandler::start_all_listeners() {
  // check db for vcans
  vector<string> vcan_list;
  dbmanager db;
  vcan_list = db.get_vcan_names();

  // check if these vcan busses are created, if not create them
  // then start a listener thread for each
  for (string vcan : vcan_list) {
    if (vcanExists(vcan) == false) {
      createVcan(vcan);
    }
    start_vcan_listener(vcan);
    sleep(1);
  }
}
