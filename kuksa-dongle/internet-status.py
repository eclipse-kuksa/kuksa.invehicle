#!/usr/bin/python3

import dbus,time
import wiringpi

wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(5, 1)
wiringpi.digitalWrite(5, 1)

status = "unregistered"
def main():

        bus = dbus.SystemBus()

        manager = dbus.Interface(bus.get_object('org.ofono', '/'),
                                                'org.ofono.Manager')

        modems = manager.GetModems()
        while True:

                for path, properties in modems:
#       print("[ %s ]" % (path))

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

                                                                for x in range(10):
                                                                        toggle(val)
                                                                break
                                        except:
                                                continue
                                else:
                                        continue

                time.sleep(6)


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

