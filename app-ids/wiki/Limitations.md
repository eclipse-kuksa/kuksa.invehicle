# Known Limitations and Next Steps
We try to maintain a list of known limitations. If there is any limitation we are not aware of, please let us know by opening an issue. 
As of now:
1. At the moment, our implementation only works for one process. If there is more than one tracer and every tracer traces a different process, then the resulting data will get mixed up ultimatively rendering the obtained dataset useless.
2. At the moment, App-IDS is meant to use a single central configuration file. This contradicts the goal of distributing the modules eventually. Nevertheless, it is already possible to distribute the deployment of modules by using multiple configuration files. However, be aware that this might introduce consistency issues, e.g., in the case of different window sizes. Please also consider to utilize multiple brokers and the [bridge feature](https://github.com/mqtt/mqtt.github.io/wiki/bridge_protocol) provided by some MQTT broker implementations or an additional adapter/relay module that manages information distribution across several brokers.
3. Deployment of files using the yocto recipes does not yet adhere to the [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0).
4. At the moment, none of the mqtt/mosquitto security capabilities are enabled.
5. We experienced hangs when enabling extensive logging and using the tool to monitor processes with a very high frequency of system calls.
6. We are currently working on a number of tests.
7. We are currently working on a tool to ease the creation and editing of the config.xml. You can already have a look at it ([MQTT-IDS-Configurator](https://github.com/SiegelDaniel/MQTT-IDS-Configurator)), however, we do not guarantee consistency with the latest xsd for the config file.
8. We are aware of the fact that there are better tracer options than strace from a performance point of view. Due to license restrictions we opted for strace in this first implementation. If you know a good tracer that can be utilized in the context of EPL compliant software, we would really appreciate your input.
