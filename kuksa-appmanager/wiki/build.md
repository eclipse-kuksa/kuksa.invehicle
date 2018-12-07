# How to build Kuksa AppManager

## Docker

Use the `build.sh` script to build docker images for **amd64**, **arm64** and **armhf** architectures.

Without arguments the script will build images for all the supported architectures. To build only a subset, you need to specify the desired architecture(s) as arguments:

    build.sh amd64

### Requirements

This script makes use of the experimental `--platform` argument to properly annotate the built images.

By default, experimental features are disabled. Edit the `/etc/docker/daemon.json` file and restart the docker engine to enable them.

```javascript
{
    "experimental": true
}
```

Please note that building docker images for other architectures requires the `qemu-user-static` package.
