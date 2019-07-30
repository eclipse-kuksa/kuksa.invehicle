# Running on Ubuntu
In this Quick Start Guide we will monitor the Firefox parent process on Ubuntu 16.04. Currently, we do not provide installation scripts modules and systemd service units. This guide is about installing the dependencies and executing the python scripts "manually". You will mainly need this during development.

## Install dependencies
We tested App-IDS with python3.5. However, it should also work with newer versions. Thus, install python, strace, mosquitto, and mosquitto-clients.
```
sudo apt update
sudo apt install python3.5 strace mosquitto mosquitto-clients
```
Reboot or start the mosquitto service unit manually.
Navigate to the root directory of App-IDS and execute
```
python3 -m pip install requirements.txt
```
to install the required python modules. A complete list with links to the modules can also be found [here](Dependencies.md).
The following steps are very similar to the steps described in the [Quick Start Guide for Kuksa](QuickStart_Kuksa.md). Thus, we keep the descriptions brief.

## Filling the database
Edit the config.xml to look as follows
```
<CONFIG>
<PNAME>firefox</PNAME>
<WINDOW_SIZE>3</WINDOW_SIZE>
<DB_HOST>../Traces.sqlite</DB_HOST>
<BROKER_IP>localhost</BROKER_IP>
<STORAGE_MODE>True</STORAGE_MODE>
<LOGGINGLEVEL>CRITICAL</LOGGINGLEVEL>
</CONFIG>
``` 
Start Firefox ;)

Navigate to the src Folder of App-IDS. Then, start each python script in an own shell. Preferably, in the following order:
```
python3 stide.py
```
```
python3 stide_syscall_formatter.py
```
```
sudo python3 syscall_tracer.py
```

After some time terminate all scripts via `SIGINT` (`control + c`).

Please note that, depending on your ```LOGGINGLEVEL```, the ```syscall_tracer``` will inform you that it found multiple processes matching the processname ```firefox```. In this case, the ```syscall_tracer``` monitors the first of those processes, which should be the parent process. The current version of App-IDS is restricted to monitor a single process which is one of the [known limitations](Limitations.md).

## Detecting anomalies
Start a fourth shell and subscribe to the `ANOMALY` topic.
```
mosquitto_sub -h localhost -t "ANOMALY"
```
Edit the config.xml to look as follows:
 ```
<CONFIG>
<PNAME>firefox</PNAME>
<WINDOW_SIZE>3</WINDOW_SIZE>
<DB_HOST>../Traces.sqlite</DB_HOST>
<BROKER_IP>localhost</BROKER_IP>
<STORAGE_MODE>False</STORAGE_MODE>
<LOGGINGLEVEL>CRITICAL</LOGGINGLEVEL>
</CONFIG>
``` 
Restart the python scripts as above.
