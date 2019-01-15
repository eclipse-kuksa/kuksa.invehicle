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

#ifndef OBECLIENT_HPP
#define OBECLIENT_HPP

#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <linux/can.h>
#include <linux/can/raw.h>
#include "common.hpp"
#include "dbmanager.hpp"
#include "vcanhandler.hpp"

#define BUFFER_SIZE 100

e_result obe_client_init();
void handle_incoming_msg(char* daa_msg);
char* prepare_outgoing_msg(char* can_msg, struct can_frame* frame);
void parse_buffer(char* msg);
void* obe_listen(void* notused);

#endif  // OBECLIENT_HPP
