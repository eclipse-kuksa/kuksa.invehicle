# Docker

## Build prerequisites


1- Enable docker experimental feature.

Create a daemon.json file in `/etc/docker/` and add 

{
 
  "experimental" : true

}

and restart docker daemon using  "systemctl restart docker"

more info [here](https://github.com/docker/docker-ce/blob/master/components/cli/experimental/README.md)

2- Install  qemu-user-static package on the host machine

 use "sudo apt-get install qemu-user-static"

## Build

Build Kuksa-compatible dockers from this app. The Dockerfile is supposed to 
be run through the magic build.sh wrapper.

To build for am64 do

`./build.sh amd64`

to build for a Pi

`/build.sh arm32v6`

If you try playing with the docker file directly, note that the build context
needs to be the toplevel of kuksa.invehicle

# Running the container
This app needs Hono credentials. It uses the following environment variables

| Variable      | What                               | 
| ------------- |------------------------------------| 
| W3CVISSURL    | URL to the W3C Server
| HONOIP        | hostname or IP of your Hono        |
| HONOPORT      | port your Hono instance listens on |   
| HONODEVICE    | Your device in Hono                |
| HONOPW        | Password for Hono                  |
| TOKEN         | Auth Token for W3C-VIS Server                   |


Example commandline

 `docker run --env W3CVISSURL='172.17.0.1:8090/vss'  --env HONOIP='11.11.11.111' --env HONOPORT='1883' --env HONODEVICE='sensor1' --env HONOPW='hono-secret' --env TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJFeGFtcGxlIEpXVCIsImlzcyI6IkVjbGlwc2Uga3Vrc2EiLCJhZG1pbiI6dHJ1ZSwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE2MDkzNzI4MDB9.lxYf-N0C66NgJiinrY_pgVpZOxgH0ppnbMsdKfNiQjbMqYTY_nEpXufmjquvBaxiYsRb_3ScXA__gmviWj_PQoU3apuMVxJjAY6xrwaXFw7g-daUi21yqLSfLptH2vqQzhA_Y1LU6u7SjeiEcGRZrgq_bHnjMM61EVDSnKGCClo' amd64/kuksa-datalogger-mqtt:7e7c437`
 


