FROM arm64v8/python:3.7-alpine AS build-env

COPY qemu-aarch64-static /usr/bin/qemu-aarch64-static

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN rm /usr/bin/qemu-aarch64-static

ADD . /app

CMD python -u -m kuksa.appmanager
