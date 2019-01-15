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

#include "obeclient.hpp"
#include "common.hpp"

int sockfd;
const char *obe_server_ip = "127.0.0.1";  //"192.168.3.40"; //
int obe_port = 6789;
int connection_status;

e_result obe_client_init() {
  pthread_t obe_thread;

  struct sockaddr_in serv_addr;

  // create socket
  sockfd = socket(AF_INET, SOCK_STREAM, 0);
  if (sockfd < 0) {
    printf("Failed to create socket\n");
    return FAILURE;
  }

  memset(&serv_addr, '0', sizeof(serv_addr));
  inet_pton(AF_INET, obe_server_ip, &serv_addr.sin_addr);
  serv_addr.sin_family = AF_INET;
  serv_addr.sin_port = htons(obe_port);

  // connect
  connection_status =
      connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr));
  if (connection_status < 0) {
    printf("Failed to connect to server\n");
    return FAILURE;
  }
  printf("Connected to server\n");

  if (pthread_create(&obe_thread, NULL, obe_listen, (void *)1) != 0) {
    perror("vcan_read thread creation failure !");
    return FAILURE;
  }

  return SUCCESS;
}

e_result obe_client_connect() {
  struct sockaddr_in serv_addr;

  // create socket
  sockfd = socket(AF_INET, SOCK_STREAM, 0);
  if (sockfd < 0) {
    printf("Failed to create socket\n");
    return FAILURE;
  }

  memset(&serv_addr, '0', sizeof(serv_addr));
  inet_pton(AF_INET, obe_server_ip, &serv_addr.sin_addr);
  serv_addr.sin_family = AF_INET;
  serv_addr.sin_port = htons(obe_port);

  // connect
  connection_status =
      connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr));
  if (connection_status < 0) {
    printf("Failed to connect to server\n");
    return FAILURE;
  }
  printf("Connected to server\n");

  return SUCCESS;
}

void *obe_listen(void *notused) {
  char buffer[BUFFER_SIZE] = {};
  while (1) {
    memset(&buffer, '\0', sizeof(buffer));

    // check connection, try to reconnect if needed
    while (connection_status < 0) {
      sleep(10);
      printf("Trying to reconnect....");
      if (obe_client_connect() == SUCCESS) {
        break;
      }
    }

    // read
    int r = read(sockfd, buffer, BUFFER_SIZE);
    if (r < 0) {
      printf("Failed to read from daa_obe server\n");
    } else if (r == 0) {
      printf("Disconnected from daa_obe server \n");
      connection_status = -1;
    } else {
      printf("daa_obe: %s\n", buffer);

      // handle msg
      parse_buffer(buffer);

      memset(&buffer, '\0', sizeof(buffer));
    }
  }
}

char *prepare_outgoing_msg(char *daa_msg, struct can_frame *frame) {
  //"{can_id|can_dlc|data[0]|data[1]}"  - can frame data
  char hex_str[50];

  strcat(daa_msg, "{");
  sprintf(hex_str, "%x", frame->can_id);
  strcat(daa_msg, hex_str);
  strcat(daa_msg, "|");
  sprintf(hex_str, "%x", frame->can_dlc);
  strcat(daa_msg, hex_str);
  strcat(daa_msg, "|");
  sprintf(hex_str, "%x", frame->data[0]);
  strcat(daa_msg, hex_str);
  strcat(daa_msg, "|");
  sprintf(hex_str, "%x", frame->data[1]);
  strcat(daa_msg, hex_str);
  strcat(daa_msg, "|");
  sprintf(hex_str, "%x", frame->data[2]);
  strcat(daa_msg, hex_str);
  strcat(daa_msg, "|");
  sprintf(hex_str, "%x", frame->data[3]);
  strcat(daa_msg, hex_str);
  strcat(daa_msg, "|");
  sprintf(hex_str, "%x", frame->data[4]);
  strcat(daa_msg, hex_str);
  strcat(daa_msg, "|");
  sprintf(hex_str, "%x", frame->data[5]);
  strcat(daa_msg, hex_str);
  strcat(daa_msg, "|");
  sprintf(hex_str, "%x", frame->data[6]);
  strcat(daa_msg, hex_str);
  strcat(daa_msg, "|");
  sprintf(hex_str, "%x", frame->data[7]);
  strcat(daa_msg, hex_str);

  strcat(daa_msg, "}");

  printf("%s\n", daa_msg);

  return daa_msg;
}

void handle_incoming_msg(char *daa_msg) {
  const char *delimiter = "|";
  struct can_frame frame;

  char *tempstr = strdup(daa_msg);

  frame.can_id = strtol(strsep(&tempstr, delimiter), NULL, 16);
  frame.can_dlc = strtol(strsep(&tempstr, delimiter), NULL, 16);
  frame.data[0] = strtol(strsep(&tempstr, delimiter), NULL, 16);
  frame.data[1] = strtol(strsep(&tempstr, delimiter), NULL, 16);
  frame.data[2] = strtol(strsep(&tempstr, delimiter), NULL, 16);
  frame.data[3] = strtol(strsep(&tempstr, delimiter), NULL, 16);
  frame.data[4] = strtol(strsep(&tempstr, delimiter), NULL, 16);
  frame.data[5] = strtol(strsep(&tempstr, delimiter), NULL, 16);
  frame.data[6] = strtol(strsep(&tempstr, delimiter), NULL, 16);
  frame.data[7] = strtol(strsep(&tempstr, delimiter), NULL, 16);

  printf("write to vcan:\n");

  // check which vcans have read permissions
  dbmanager db;
  vector<string> vcan_list =
      db.select_vcans_from_read_table(frame.can_id & 0x1FFFFFFF);
  for (string vcan : vcan_list) {
    // write to vcan;
    cout << "write to vcan: " << vcan << endl;
    vcanlistener listener(vcan);
    listener.vcan_socket_init();
    listener.vcan_write_frame(&frame);
  }
}

void parse_buffer(char *msg) {
  int i = 0;
  size_t sindex = -1;
  size_t eindex = -1;
  char daa_msg[BUFFER_SIZE];

  // locate msg start-endpoints
  while (msg[i] != '\0') {
    if (msg[i] == '{') sindex = i + 1;

    if (msg[i] == '}') {
      eindex = i;
      break;
    }
    i++;
  }

  // check endpoints
  if (sindex > 0 && eindex > 2) {
    memcpy(daa_msg, &msg[sindex], eindex - sindex);
    daa_msg[eindex - 1] = '\0';

    handle_incoming_msg(daa_msg);

    daa_msg[0] = '\0';

    if (eindex + 1 != strlen(msg))
      parse_buffer(&msg[eindex + 1]);
    else {
      printf("...\n");
      return;
    }
  } else {
    printf("...\n");
    return;
  }
}
