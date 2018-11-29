#  Copyright (c) 2018 Eclipse KUKSA project
#
#  This program and the accompanying materials are made available under the
#  terms of the Eclipse Public License 2.0 which is available at
#  http://www.eclipse.org/legal/epl-2.0
#
#  SPDX-License-Identifier: EPL-2.0
#
#  Contributors: Robert Bosch GmbH
#
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0
#
# SPDX-License-Identifier: EPL-2.0
#
# Contributors: Robert Bosch GmbH

import logging
import re
from threading import Thread
from typing import Callable

import paho.mqtt.client as mqtt


class Config:
    def __init__(self, server: str, username: str, password: str):
        self.server_host = server.split(":")[0]
        self.server_port = int(server.split(":")[1])
        self.username = username
        self.password = password


class Client(mqtt.Client):
    def __init__(self, config: Config, handle_config_changed: Callable[[str], None]):
        super(Client, self).__init__()

        self.logger = logging.getLogger('{}.{}'.format(self.__class__.__module__, self.__class__.__name__))
        self.config = config
        self.handle_config_changed = handle_config_changed

        self.enable_logger()
        self.username_pw_set(config.username, config.password)

    def start(self):
        thread = Thread(name='HonoClient', target=self.__run__, daemon=True)
        thread.start()

    def __run__(self):
        self.connect(self.config.server_host, self.config.server_port, 60)
        self.loop_forever()

    def on_connect(self, *args, **kwargs):
        self.subscribe('control/+/+/req/#')

    def on_message(self, client, userdata, message: mqtt.MQTTMessage):
        self.logger.info('Message')

        topic_params = re.compile(r'control///req/([^/]+)/([^/]+).*').match(message.topic)
        if topic_params:
            req_id = topic_params.group(1)
            command = topic_params.group(2)
            payload = message.payload

            status = 404
            if command == 'kuksa-config-changed':
                self.handle_config_changed('hono')
                status = 200

            reply_topic = 'control///res/{req_id}/{status}'.format(req_id=req_id, status=status)
            self.publish(reply_topic)
