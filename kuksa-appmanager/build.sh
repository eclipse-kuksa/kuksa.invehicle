#!/usr/bin/env bash

VERSION=`grep __version__ kuksa/appmanager/__init__.py | sed -n "s/.*'\([^']\+\).*/\1/p"`
if [ -z "$VERSION" ]; then
    echo "Failed to extract version string" 1>&2
    exit 1
fi

EXPERIMENTAL=`docker version | grep Experimental | tail -n 1 | xargs`
if [ "$EXPERIMENTAL" != "Experimental: true" ]; then
    echo "Please enable the docker engine's experimental features" 1>&2
    exit 1
fi

function build {
    TARGET=$1

    # generate Dockerfile.build
    case ${TARGET} in
    'amd64')
        sed -e "s/arm64v8/amd64/g" Dockerfile > Dockerfile.build
        sed -i -e "s/^.*qemu-aarch64-static.*$//g" Dockerfile.build
        ;;
    'arm64')
        cp /usr/bin/qemu-aarch64-static ./
        if [ "$?" != "0" ]; then
            echo "Please install the qemu-user-static package" 1>&2
            exit 1
        fi
        cp Dockerfile Dockerfile.build
        ;;
    'armhf')
        cp /usr/bin/qemu-arm-static ./
        if [ "$?" != "0" ]; then
            echo "Please install the qemu-user-static package" 1>&2
            exit 1
        fi
        sed -e "s/arm64v8/armhf/g" Dockerfile > Dockerfile.build
        sed -i -e "s/qemu-aarch64-static/qemu-arm-static/g" Dockerfile.build
        ;;
    esac

    # build image
    docker build --platform linux/$TARGET -f ./Dockerfile.build -t ${TARGET}/kuksa-appmanager:${VERSION} .

    # cleanup
    rm -f Dockerfile.build
    rm -f qemu-aarch64-static
    rm -f qemu-arm-static
}

build 'amd64'
build 'arm64'
build 'armhf'
