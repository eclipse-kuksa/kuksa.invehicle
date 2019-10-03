# Kuksa AppManager

The AppManager is a python client that uses HawkBit artifacts to launch apps as Docker containers or AGL widgets.

Once started, the AppManager will check regularly with HawkBit for required actions, covering deployment and configuration data. Additionally a MQTT connection
to Hono is used to receive `configuration change` events that trigger deployment actions.

Currently, two types of app artifacts are supported. Docker containers and AGL widgets.
A Docker container must contain a `docker-container.json` artifact.
The AppManager uses this JSON file to to pull images from a Docker registry and create containers.
An AGL widget must have an artifact with the `*.wgt` file extension.

#### Hello world app

```json
{
    "image": "alpine:latest",
    "config": {
        "command": "sh -c \"while :; do echo 'Hello world'; sleep 1; done\"",
        "tty": true
    }
}
```

## Resources

- [Development](wiki/development.md)
- [Build](wiki/build.md)
- [FOTA](wiki/fota.md)
- [AGL Widgets](wiki/widgets.md)
- [AGL Recipe](wiki/agl.md)

### Note

If you can not see your target in the [Appstore](https://github.com/eclipse/kuksa.cloud/tree/master/kuksa-appstore), make sure that your `AppstoreUsername` is included in the Description box of your target in Eclipse HawkBit. This is intended to be automated in the future (https://github.com/eclipse/kuksa.invehicle/issues/92).
