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

#include "dbmanager.hpp"

dbmanager::dbmanager() {
  rc = sqlite3_open("daa.db", &db);

  if (rc) {
    cout << "Can't open database: " << sqlite3_errmsg(db) << "\n";
  } else {
    sqlite3_exec(db, "PRAGMA foreign_keys = ON;", 0, 0, 0);
  }
}

dbmanager::~dbmanager() { sqlite3_close(db); }

void dbmanager::insert_into_read_table(string vcan_name, int canid) {
  char *zErrMsg = 0;

  stringstream ss;
  ss << "INSERT INTO READ VALUES(\"" << vcan_name << "\"," << canid << ");";

  rc = sqlite3_exec(db, ss.str().c_str(), NULL, 0, &zErrMsg);
  if (rc != SQLITE_OK) {
    cout << "SQL error: " << sqlite3_errmsg(db) << endl;
    sqlite3_free(zErrMsg);
  } else {
    cout << "SQL: insert_into_vcan_table successful" << endl;
  }
}

void dbmanager::insert_into_write_table(string vcan_name, int canid) {
  char *zErrMsg = 0;

  stringstream ss;
  ss << "INSERT INTO WRITE VALUES(\"" << vcan_name << "\"," << canid << ");";

  rc = sqlite3_exec(db, ss.str().c_str(), NULL, 0, &zErrMsg);
  if (rc != SQLITE_OK) {
    cout << "SQL error: " << sqlite3_errmsg(db) << endl;
    sqlite3_free(zErrMsg);
  } else {
    cout << "SQL: insert_into_vcan_table successful" << endl;
  }
}

void dbmanager::insert_into_vcan_table(string vcan_name) {
  char *zErrMsg = 0;

  stringstream ss;
  ss << "INSERT INTO VCAN VALUES(NULL,\"" << vcan_name << "\");";

  rc = sqlite3_exec(db, ss.str().c_str(), NULL, 0, &zErrMsg);
  if (rc != SQLITE_OK) {
    cout << "SQL error: " << sqlite3_errmsg(db) << endl;
    sqlite3_free(zErrMsg);
  } else {
    cout << "SQL: insert_into_vcan_table successful" << endl;
  }
}

void dbmanager::delete_vcan(string vcan_name) {
  char *zErrMsg = 0;

  stringstream ss;
  ss << "DELETE FROM VCAN WHERE NAME = \"" << vcan_name << "\";";

  rc = sqlite3_exec(db, ss.str().c_str(), NULL, 0, &zErrMsg);
  if (rc != SQLITE_OK) {
    cout << "SQL error: " << sqlite3_errmsg(db) << endl;
    sqlite3_free(zErrMsg);
  } else {
    cout << "SQL: delete_from_vcan_table successful" << endl;
  }
}

vector<int> dbmanager::get_read_rules(string vcan_name) {
  char *zErrMsg = 0;
  stringstream ss;
  vector<int> results;
  sqlite3_stmt *stmt;

  ss << "SELECT CANID FROM READ WHERE VCAN_NAME = \"" << vcan_name << "\";";
  rc = sqlite3_prepare_v2(db, ss.str().c_str(), -1, &stmt, NULL);

  if (rc != SQLITE_OK) {
    cout << "SQL error: " << sqlite3_errmsg(db) << endl;
    sqlite3_free(zErrMsg);
    return results;
  }
  rc = sqlite3_step(stmt);
  while (rc != SQLITE_DONE) {
    results.push_back(sqlite3_column_int(stmt, 0));
    rc = sqlite3_step(stmt);
  }

  sqlite3_finalize(stmt);
  return results;
}

vector<int> dbmanager::get_write_rules(string vcan_name) {
  char *zErrMsg = 0;
  stringstream ss;
  vector<int> results;
  sqlite3_stmt *stmt;

  ss << "SELECT CANID FROM WRITE WHERE VCAN_NAME = \"" << vcan_name << "\";";
  // cout << ss.str() << endl;
  rc = sqlite3_prepare_v2(db, ss.str().c_str(), -1, &stmt, NULL);

  if (rc != SQLITE_OK) {
    cout << "SQL error: " << sqlite3_errmsg(db) << endl;
    sqlite3_free(zErrMsg);
    return results;
  }
  rc = sqlite3_step(stmt);
  while (rc != SQLITE_DONE) {
    results.push_back(sqlite3_column_int(stmt, 0));
    rc = sqlite3_step(stmt);
  }

  sqlite3_finalize(stmt);
  return results;
}

vector<string> dbmanager::get_vcan_names() {
  char *zErrMsg = 0;
  stringstream ss;
  vector<string> results;
  sqlite3_stmt *stmt;

  ss << "SELECT NAME FROM VCAN;";
  rc = sqlite3_prepare_v2(db, ss.str().c_str(), -1, &stmt, NULL);

  if (rc != SQLITE_OK) {
    cout << "SQL error: " << sqlite3_errmsg(db) << endl;
    sqlite3_free(zErrMsg);
    return results;
  }
  rc = sqlite3_step(stmt);
  while (rc != SQLITE_DONE) {
    results.push_back((const char *)sqlite3_column_text(stmt, 0));
    rc = sqlite3_step(stmt);
  }

  sqlite3_finalize(stmt);
  return results;
}

vector<string> dbmanager::select_vcans_from_read_table(int canid) {
  char *zErrMsg = 0;
  stringstream ss;
  vector<string> results;
  sqlite3_stmt *stmt;

  ss << "SELECT VCAN_NAME FROM READ WHERE CANID = " << canid << ";";
  rc = sqlite3_prepare_v2(db, ss.str().c_str(), -1, &stmt, NULL);

  if (rc != SQLITE_OK) {
    cout << "SQL error: " << sqlite3_errmsg(db) << endl;
    sqlite3_free(zErrMsg);
    return results;
  }
  rc = sqlite3_step(stmt);
  while (rc != SQLITE_DONE) {
    results.push_back((const char *)sqlite3_column_text(stmt, 0));
    rc = sqlite3_step(stmt);
  }

  sqlite3_finalize(stmt);
  return results;
}

vector<string> dbmanager::select_vcans_from_write_table(int canid) {
  char *zErrMsg = 0;
  stringstream ss;
  vector<string> results;
  sqlite3_stmt *stmt;

  ss << "SELECT VCAN_NAME FROM WRITE WHERE CANID = " << canid << ";";
  rc = sqlite3_prepare_v2(db, ss.str().c_str(), -1, &stmt, NULL);

  if (rc != SQLITE_OK) {
    cout << "SQL error: " << sqlite3_errmsg(db) << endl;
    sqlite3_free(zErrMsg);
    return results;
  }
  rc = sqlite3_step(stmt);
  while (rc != SQLITE_DONE) {
    results.push_back((const char *)sqlite3_column_text(stmt, 0));
    rc = sqlite3_step(stmt);
  }

  sqlite3_finalize(stmt);
  return results;
}

void dbmanager::store_read_rules(string vcan_name, json can_json) {
  auto perms = can_json["read"].as<std::deque<std::string>>();
  for (auto r : perms) {
    this->insert_into_read_table(vcan_name, stoi(r));
  }
}

void dbmanager::store_write_rules(string vcan_name, json can_json) {
  auto perms = can_json["write"].as<std::deque<std::string>>();
  for (auto r : perms) {
    this->insert_into_write_table(vcan_name, stoi(r));
  }
}
