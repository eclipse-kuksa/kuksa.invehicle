#!/bin/sh                                                                                                                                                                         
#                                                                                                                                                                                 
# Copyright (c) 2018 Eclipse KUKSA project                                                                                                                                        
#                                                                                                                                                                                 
# This program and the accompanying materials are made available under the                                                                                                        
# terms of the Eclipse Public License 2.0 which is available at                                                                                                                   
# http://www.eclipse.org/legal/epl-2.0                                                                                                                                            
#                                                                                                                                                                                 
# SPDX-License-Identifier: EPL-2.0                                                                                                                                                
# Forever checker for people so poor that they do not even have cron                                                                                                              
#                                                                                                                                                                                 
# Contributors: Robert Bosch GmbH                                                                                                                                                 
                                                                                                                                                                                  
DELAY=5                                                                                                                                                                           
                                                                                                                                                                                  
coproc pwd                                                                                                                                                                        
DIR=$(cat <&"${COPROC[0]}")                                                                                                                                                       
pwd                                                                                                                                                                               
mkdir /usr/apps                                                                                                                                                                                  
while true;                                                                                                                                                                       
do                                                                                                                                                                                
        echo "Checking...."                                                                                                                                                       
        python3 $DIR/CheckNewSoftware.py                                                                                                                                          
        sleep $DELAY                                                                                                                                                              
done
