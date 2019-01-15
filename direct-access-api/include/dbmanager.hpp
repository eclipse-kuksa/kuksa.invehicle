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

#ifndef DBMANAGER_H
#define DBMANAGER_H

#include <iostream>
#include <sqlite3.h>
#include <sstream>
#include <vector>
#include <jsoncons/json.hpp>

using namespace std;

using namespace jsoncons;
using jsoncons::json;

class dbmanager {
 private:
  int rc;
  sqlite3 *db;

 public:
  dbmanager();
  ~dbmanager();
  void store_read_rules(string vcan_name, json can_json);
  void store_write_rules(string vcan_name, json can_json);
  void insert_into_read_table(string vcan_name, int canid);
  void insert_into_write_table(string vcan_name, int canid);
  void insert_into_vcan_table(string vcan_name);
  vector<int> get_read_rules(string vcan_name);
  vector<int> get_write_rules(string vcan_name);
  vector<string> get_vcan_names();

  void delete_vcan(string vcan_name);

  vector<string> select_vcans_from_read_table(int canid);
  vector<string> select_vcans_from_write_table(int canid);
};

#endif  // DBMANAGER_H
