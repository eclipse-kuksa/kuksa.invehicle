#Building everything
FROM arm64v8/alpine:3.8 AS build-env

COPY qemu-aarch64-static /usr/bin/qemu-aarch64-static

RUN apk update && apk add alpine-sdk cmake  boost-dev openssl-dev

ADD . /app
WORKDIR /app/datalogger-mqtt

RUN rm -rf build && mkdir build && cd build && cmake ../
RUN cd build && make



#Transferring build artifacts to minimal docker
FROM arm64v8/alpine:3.8
RUN apk update && apk add openssl boost-system boost-thread libstdc++
COPY --from=build-env /app/datalogger-mqtt/build/datalogger-mqtt /
COPY --from=build-env /app/datalogger-mqtt/docker/dockerentry.sh /
COPY --from=build-env /app/datalogger-mqtt/build/CA.pem /
COPY --from=build-env /app/datalogger-mqtt/build/Client.key /
COPY --from=build-env /app/datalogger-mqtt/build/Client.pem /

WORKDIR /
CMD /bin/sh /dockerentry.sh
