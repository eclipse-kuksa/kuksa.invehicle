#!/usr/bin/python3                                                                                                                                                                                          
                                                                                                                                                                                                            
import dbus                                                                                                                                                                                                 
import sys                                                                                                                                                                                                  
import os

os.system("sleep 20s")                                                                                                                                                                                                           
bus = dbus.SystemBus()

try:                                                                                                                                                                                      
                                                                                                                                                                                                            
   if len(sys.argv) == 2:                                                                                                                                                                                      
           path = sys.argv[1]                                                                                                                                                                                  
   else:                                                                                                                                                                                                       
           manager = dbus.Interface(bus.get_object('org.ofono', '/'),                                                                                                                                          
                        'org.ofono.Manager')                                                                                                                                                                
           modems = manager.GetModems()                                                                                                                                                                        
           path = modems[0][0]                                                                                                                                                                                 
                                                                                                                                                                                                            
   print("Connecting modem %s..." % path)                                                                                                                                                                      
   modem = dbus.Interface(bus.get_object('org.ofono', path),                                                                                                                                                   
                                                'org.ofono.Modem')                                                                                                                                          
                                                                                                                                                                                                            
   modem.SetProperty("Powered", dbus.Boolean(1), timeout = 120)
except:
   print("ofono has not started properly. This is a bug from ofono side. I ll try to fix this by restarting ofono")
   os.system("systemctl restart ofono")
