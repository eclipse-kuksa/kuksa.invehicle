#Building everything
FROM arm64v8/alpine:3.8 AS build-env

COPY datalogger-mqtt/docker/qemu-aarch64-static /usr/bin/qemu-aarch64-static

RUN apk update && apk add cmake alpine-sdk boost-dev boost-system boost-thread openssl-dev libstdc++

ADD . /app
WORKDIR /app/datalogger-mqtt

RUN rm -rf build && mkdir build && cd build && cmake ../
RUN cd build && make



#Transferring build artifacts to minimal docker
FROM arm64v8/alpine:3.8
#For debugging uncomment, and replae copy with real install to see what is missing... 
#RUN apk update && apk add openssl boost-system boost-thread libstdc++ 
COPY --from=build-env /lib/libssl.so.1.0.0   /lib/
COPY --from=build-env /lib/libcrypto.so.1.0.0  /lib/
COPY --from=build-env /usr/lib/libstdc++.so.6  /usr/lib/
COPY --from=build-env /usr/lib/libgcc_s.so.1 /usr/lib/


COPY --from=build-env /app/datalogger-mqtt/build/datalogger-mqtt /
COPY --from=build-env /app/datalogger-mqtt/docker/dockerentry.sh /
COPY --from=build-env /app/datalogger-mqtt/build/CA.pem /
COPY --from=build-env /app/datalogger-mqtt/build/Client.key /
COPY --from=build-env /app/datalogger-mqtt/build/Client.pem /

WORKDIR /
CMD /bin/sh /dockerentry.sh
