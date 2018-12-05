#!/usr/bin/env bash

VERSION=1.1

function build {
    TARGET=$1

    # generate Dockerfile.build
    case ${TARGET} in
    'amd64')
        sed -e "s/arm64v8/amd64/g" Dockerfile > Dockerfile.build
        sed -i -e "s/^.*qemu-aarch64-static.*$//g" Dockerfile.build
        ;;
    'arm64')
        cp Dockerfile Dockerfile.build
        cp /usr/bin/qemu-aarch64-static ./
        ;;
    'armhf')
        sed -e "s/arm64v8/armhf/g" Dockerfile > Dockerfile.build
        sed -i -e "s/qemu-aarch64-static/qemu-arm-static/g" Dockerfile.build
        cp /usr/bin/qemu-arm-static ./
        ;;
    esac

    # build image
    docker build -f ./Dockerfile.build -t kuksaregistry.azurecr.io/kuksa/${TARGET}/client:${VERSION} .
}

build 'amd64'
build 'arm64'
build 'armhf'

rm -f Dockerfile.build
rm -f qemu-aarch64-static
rm -f qemu-arm-static