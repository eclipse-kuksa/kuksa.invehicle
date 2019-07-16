#!/usr/bin/python3         
                              
import dbus,time,os,sys     
import wiringpi                                           
                              
wiringpi.wiringPiSetupGpio()                                                      
wiringpi.pinMode(5, 1)                                              
wiringpi.digitalWrite(5, 1)                                                       
                                                                                  
status = "unregistered"                                             
current_tech = ""                                      
def main():                                                  
        global current_tech                                                  
        bus = dbus.SystemBus()                               
        while True:                                                               
                print("current tech is %s" % current_tech)                        
                try:                                                     
                        manager = dbus.Interface(bus.get_object('org.ofono', '/'),
                                                'org.ofono.Manager')  
                        modems = manager.GetModems()                 
                        for path, properties in modems:                   
                                print("[ %s ]" % (path))                                          
                                                                                  
                                for key in properties.keys():                                     
                                        if key in ["Interfaces", "Features"]:                     
                                                val = ""                                  
                                                for i in properties[key]:
                                                        val += i + " "                     
                                        else:                                             
                                                val = properties[key]                      
#               print("    %s = %s" % (key, val))                                                 
                                                                                                     
                                for interface in properties["Interfaces"]:                                         
                                        object = dbus.Interface(bus.get_object('org.ofono', path),   
                                                                        interface)                                           
                                                                                                                   
#               print("    [ %s ]" % (interface))                                                                            
                                        if interface in ["org.ofono.NetworkRegistration"]:                                   
                                                try:                                       
                                                        properties = object.GetProperties()    
                                                        for key in properties.keys():                              
                                                                global status                                      
                                                                if key == "Status" :                                                                                                                        
                                                                        status = str(properties[key])                                                                
                                                                elif status == "registered" and key == "Strength" :                                                                                         
                                                                        val = properties[key]                                                                                                               
                                                                        print("Network registered with %s = %d" % (key, val))                                        
                                                                                                                   
                                                                        for x in range(25):                        
                                                                                toggle(val)                        
                                                                elif key == "Technology" :                         
                                                                        if current_tech == "" :                                                                                                             
                                                                                current_tech = str(properties[key])                                                                                         
                                                                        elif current_tech != str(properties[key]):                                                   
                                                                                print("Technology changed from %s to %s. This case does not work without re-enabling internet context" % (current_tech, str(properties[key])))
                                                                                os.system("cd /usr/lib/ofono/test ; ./activate-context ; ./process-context-settings")
                                                                                time.sleep(5)
                                                                                current_tech = str(properties[key])
                                                except: 
                                                        continue
                                        else:                
                                                continue     
                except:           
                        print("ofono not available on d-bus")
                sys.stdout.flush() 
                time.sleep(4)      



def toggle (strength):
        delay = float(strength) + 1
        delay = 3/delay
#       print(delay)
        time.sleep(delay)
        wiringpi.digitalWrite(5, 0)
        time.sleep(delay)
        wiringpi.digitalWrite(5, 1)

if __name__ == "__main__":                                                                                                                                                                                  
        main()

