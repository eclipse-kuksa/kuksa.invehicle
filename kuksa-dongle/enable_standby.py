# Copyright (c) 2019 Eclipse KUKSA project
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0
#
# SPDX-License-Identifier: EPL-2.0
#
# Contributors: Robert Bosch GmbH
import wiringpi
import os, time

wiringpi.wiringPiSetupGpio()
wiringpi.pullUpDnControl(7,2) # Pull up internal resistor enable GPIO7
wiringpi.pinMode(7, 1) # Set GPIO7 as Output pin
wiringpi.digitalWrite(7, 0) # Set should be set to 0
wiringpi.pullUpDnControl(9,2) # Pull up enable GPIO9
wiringpi.pinMode(9, 0)

while(True):
   stn_sleep = wiringpi.digitalRead(9)
   if(stn_sleep == 1) :
      os.system("halt")
   time.sleep(1)         


#wiringpi.digitalWrite(7, 1) # Write 1 to GPIO7 to Remove voltage to Pi
