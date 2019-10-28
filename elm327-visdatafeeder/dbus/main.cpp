/*
 * ******************************************************************************
 * Copyright (c) 2019 Robert Bosch GmbH and others.
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

#include <string.h>
#include <stdlib.h>
#include <iostream>

#include <sys/types.h>
#include <unistd.h>

#include <time.h>
#include <gio/gio.h>
#include "vssMapper.hpp"
#include "obd.hpp"

using namespace std;

volatile bool stopLoop = false;
GDBusConnection *dbus_connection = NULL;
gchar *dbus_owner_name =  NULL;

// Cmd line parameters
char PORT[128];
int AVTHREADSLEEP;
int DTCTHREADSLEEP;

// Publishes signed integer value to w3c-visserver.
static void
publishInt (const gchar* path , const int64_t value)
{
  if ((dbus_connection == NULL) || (dbus_owner_name == NULL)) {
     cout << "D bus connection doesnt seem exist anymore." << endl;
     return;
  }
  
  GDBusMessage *method_call_message;

  method_call_message = NULL;
  method_call_message = g_dbus_message_new_method_call (dbus_owner_name,
                                                        "/org/eclipse/kuksaW3Cbackend",
                                                        "org.eclipse.kuksa.w3cbackend",
                                                        "pushInt");
  // Append method parameters
  g_dbus_message_set_body (method_call_message, g_variant_new ("(sx)", path , value));
  
  g_dbus_connection_send_message_with_reply       (dbus_connection,
                                                   method_call_message,
                                                   G_DBUS_SEND_MESSAGE_FLAGS_NONE,
                                                   -1,
                                                   NULL, /* out_serial */
                                                   NULL, /* cancellable */
                                                   NULL,
                                                   NULL);
  
  g_object_unref (method_call_message);
}

// Publishes unsigned integer value to w3c-visserver.
static void
publishUnsignedInt (const gchar* path , const uint64_t value)
{
  if ((dbus_connection == NULL) || (dbus_owner_name == NULL)) {
     cout << "D bus connection doesnt seem exist anymore." << endl;
     return;
  }
  
  GDBusMessage *method_call_message;

  method_call_message = NULL;
  method_call_message = g_dbus_message_new_method_call (dbus_owner_name,
                                                        "/org/eclipse/kuksaW3Cbackend",
                                                        "org.eclipse.kuksa.w3cbackend",
                                                        "pushUnsignedInt");
  // Append method parameters
  g_dbus_message_set_body (method_call_message, g_variant_new ("(st)", path , value));
  
  g_dbus_connection_send_message_with_reply       (dbus_connection,
                                                   method_call_message,
                                                   G_DBUS_SEND_MESSAGE_FLAGS_NONE,
                                                   -1,
                                                   NULL, /* out_serial */
                                                   NULL, /* cancellable */
                                                   NULL,
                                                   NULL);
  
  g_object_unref (method_call_message);
}


// Publishes double or float value to w3c-visserver.
static void
publishDouble (const gchar* path , const double value)
{
  if ((dbus_connection == NULL) || (dbus_owner_name == NULL)) {
     cout << "D bus connection doesnt seem exist anymore." << endl;
     return;
  }
  
  GDBusMessage *method_call_message;

  method_call_message = NULL;
  method_call_message = g_dbus_message_new_method_call (dbus_owner_name,
                                                        "/org/eclipse/kuksaW3Cbackend",
                                                        "org.eclipse.kuksa.w3cbackend",
                                                        "pushDouble");
  // Append method parameters
  g_dbus_message_set_body (method_call_message, g_variant_new ("(sd)", path , value));
  
  g_dbus_connection_send_message_with_reply       (dbus_connection,
                                                   method_call_message,
                                                   G_DBUS_SEND_MESSAGE_FLAGS_NONE,
                                                   -1,
                                                   NULL, /* out_serial */
                                                   NULL, /* cancellable */
                                                   NULL,
                                                   NULL);
  
  g_object_unref (method_call_message);
}



// Publishes Boolean value to w3c-visserver.
static void
publishBool (const gchar* path , const bool value)
{
  if ((dbus_connection == NULL) || (dbus_owner_name == NULL)) {
     cout << "D bus connection doesnt seem exist anymore." << endl;
     return;
  }
  
  GDBusMessage *method_call_message;

  method_call_message = NULL;
  method_call_message = g_dbus_message_new_method_call (dbus_owner_name,
                                                        "/org/eclipse/kuksaW3Cbackend",
                                                        "org.eclipse.kuksa.w3cbackend",
                                                        "pushBool");
  // Append method parameters
  g_dbus_message_set_body (method_call_message, g_variant_new ("(sb)", path , value));
  
  g_dbus_connection_send_message_with_reply       (dbus_connection,
                                                   method_call_message,
                                                   G_DBUS_SEND_MESSAGE_FLAGS_NONE,
                                                   -1,
                                                   NULL, /* out_serial */
                                                   NULL, /* cancellable */
                                                   NULL,
                                                   NULL);
  
  g_object_unref (method_call_message);
}

// Publishes string value to w3c-visserver.
static void
publishString (const gchar* path , string value)
{
  if ((dbus_connection == NULL) || (dbus_owner_name == NULL)) {
     cout << "D bus connection doesnt seem exist anymore." << endl;
     return;
  }
  
  GDBusMessage *method_call_message;

  method_call_message = NULL;
  method_call_message = g_dbus_message_new_method_call (dbus_owner_name,
                                                        "/org/eclipse/kuksaW3Cbackend",
                                                        "org.eclipse.kuksa.w3cbackend",
                                                        "pushString");
  // Append method parameters
  g_dbus_message_set_body (method_call_message, g_variant_new ("(ss)", path , value.c_str()));
  
  g_dbus_connection_send_message_with_reply       (dbus_connection,
                                                   method_call_message,
                                                   G_DBUS_SEND_MESSAGE_FLAGS_NONE,
                                                   -1,
                                                   NULL, /* out_serial */
                                                   NULL, /* cancellable */
                                                   NULL,
                                                   NULL);
  
  g_object_unref (method_call_message);
}

// P_Thread function
void *startLoop(void *arg) {
  connectOBD(10);
  // Sleep 50ms.
  usleep(50000);
  //Do the looping here.
  while (!stopLoop) {
      // Sleep between values.
      
      int rpm = getRPM();
      if (rpm > -1)
         publishDouble("Vehicle.OBD.EngineSpeed",rpm);

      usleep(AVTHREADSLEEP);
      
      int speed = getVehicleSpeed();
      if (speed > -1)
         publishInt("Vehicle.OBD.Speed",speed);

      usleep(AVTHREADSLEEP);
      
  }
}

// start the mail loop thread. 
int startLoopThread() {
  pthread_t elm327loop_thread;
  stopLoop = false;
  /* create the web socket server thread. */
  if (pthread_create(&elm327loop_thread, NULL, &startLoop, NULL)) {
    cout << "main: Error creating main loop thread " << endl;
    return -1;
  }
  return 0;
}

void stopLoopThread() {
   stopLoop = true;
}


static void
on_name_appeared (GDBusConnection *connection,
                  const gchar     *name,
                  const gchar     *name_owner,
                  gpointer         user_data)
{
  
  dbus_connection = connection;
  dbus_owner_name = (gchar*)name_owner;

  int res = startLoopThread();

  if (res != 0) {
     cout << "Something went wrong while starting the main loop thread "<< endl;
  }
}


static void
on_name_vanished (GDBusConnection *connection,
                  const gchar     *name,
                  gpointer         user_data)
{
  g_printerr ("Failed to get name owner for %s\n"
              "Is w3c-visserver running?\n",
              name);
  // Stop thread here.
  stopLoopThread();
  dbus_connection = NULL;
  dbus_owner_name = NULL; 
  exit (1);
}


int
main (int argc, char *argv[])
{
  if (argc == 5) {
    strcpy(PORT, argv[1]);
    AVTHREADSLEEP = atoi(argv[3]);
    DTCTHREADSLEEP = atoi(argv[4]);
  } else {
    cerr << "Usage ./elm327_visfeeder <ELM327-PORT> <TOKEN>"
            "<AVTHREADDELAY> <DTCTHREADDELAY>"
         << endl;
    return -1;
  }

  guint watcher_id;
  GMainLoop *loop;

 

  watcher_id = g_bus_watch_name (G_BUS_TYPE_SYSTEM,
                                 "org.eclipse.kuksa.w3cbackend",
                                 G_BUS_NAME_WATCHER_FLAGS_NONE,
                                 on_name_appeared,
                                 on_name_vanished,
                                 NULL,
                                 NULL);
  
  

  loop = g_main_loop_new (NULL, FALSE);
  g_main_loop_run (loop);

  g_bus_unwatch_name (watcher_id);
  return 0;
}

