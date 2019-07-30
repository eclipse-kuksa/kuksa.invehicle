
# Running on AGL with agl-kuksa
In this Quick Start Guide we will monitor the HomeScreen process of Automotive Grade Linux (AGL). 

## Building the Image
App-IDS is part of the Kuksa Layer for yocto. Following the instructions for [agl-kuksa](https://github.com/eclipse/kuksa.invehicle/tree/master/agl-kuksa "agl-kuksa") results in an AGL image for Raspberry Pi 3 that encompasses the App-IDS modules and systemd service units to start and stop the modules. 

## Filling the database
Configuration of App-IDS is done via a central configuration file. You can ssh to your Raspberry and update the configuration file using, e.g., ```vi```

 ```
 vi /usr/bin/app-ids/src/config.xml
 ```

To monitor the HomeScreen your ```config.xml``` should look as follows:
```
<CONFIG>
<PNAME>HomeScreen</PNAME>
<WINDOW_SIZE>3</WINDOW_SIZE>
<DB_HOST>../Traces.sqlite</DB_HOST>
<BROKER_IP>localhost</BROKER_IP>
<STORAGE_MODE>True</STORAGE_MODE>
<LOGGINGLEVEL>CRITICAL</LOGGINGLEVEL>
</CONFIG>
``` 
In comparison to the sample `config.xml` we defined HomeScreen as the name of the process we want to monitor. The remaining relevant fields for this quick start guide are:
- `WINDOW_SIZE` is the size of the system call windows used by STIDE
- `DB_HOST` is the location of the sqlite database file
- `BROKER_IP` the ip of the mqtt broker. As the image is build with mosquitto, localhost works just fine here.
- `STORAGE_MODE` 
	- `True` indicates that we want to fill the database with system call sequences representing benign behavior
	- `False` indicates that we want to compare monitored systems calls with the database to find anomalies

To start filling up your database simply start the **stide** service using:
``` 
systemctl start stide
```
This also starts the **__systemcall_tracer__** and **__stide_syscall_formatter__** modules. Correspondingly, you can use 
```
systemctl stop stide
```
to stop the services and finish filling your database.

## Detecting anomalies
Detected anomalies are published on the `ANOMALY` mqtt topic. So, it is a good idea to subscribe to this topic on your **local machine**. The simplest way to do this is using the ```mosquitto-clients``` package. After you installed the package you can simply subscribe with:
```
mosquitto_sub -h <ip_of_your_raspberry> -t "ANOMALY"
```

Now, we have to configure the **stide** module to detect anomalies. Thus, `config.xml` should look as follows:
 ```
<CONFIG>
<PNAME>HomeScreen</PNAME>
<WINDOW_SIZE>3</WINDOW_SIZE>
<DB_HOST>../Traces.sqlite</DB_HOST>
<BROKER_IP>localhost</BROKER_IP>
<STORAGE_MODE>False</STORAGE_MODE>
<LOGGINGLEVEL>CRITICAL</LOGGINGLEVEL>
</CONFIG>
``` 

Then, restart the service:
```
systemctl start stide
```
If you already filled your database extensively, meaning it covers the benign behavior to a large extend, you will obviously not see any anomalies, unless somebody starts tampering with the process. However, for testing purposes you can simply try to only fill the database for a short time or even use an empty one.

