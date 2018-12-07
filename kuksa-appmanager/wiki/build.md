# How to build Kuksa AppManager

## Docker

Use the `build.sh` script to build docker images for amd64, arm64 and armhf architectures.

This script makes use of the experimental `--platform` argument to properly annotate the built images.

By default, experimental features are disabled. Edit the `/etc/docker/daemon.json` file and restart the docker engine to enable them.

    {
        "experimental": true
    }

Please note that building docker images for other architectures requires the 'qemu-user-static' package.
