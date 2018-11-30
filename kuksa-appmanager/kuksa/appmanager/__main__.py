# Copyright (c) 2018 Eclipse KUKSA project
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0
#
# SPDX-License-Identifier: EPL-2.0
#
# Contributors: Robert Bosch GmbH

import logging
import os

from . import hawkbit
from . import hono

logging.basicConfig(format='%(asctime)s - %(threadName)s - %(levelname)s - %(name)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger('kuksa.appmanager')

__missing_config_detected = False


def __get_config_value(name, default_value=None, value_type: type = str):
    value = os.getenv(name)
    if value is None:
        if default_value is None:
            global __missing_config_detected
            __missing_config_detected = True
            logger.error("Missing environment variable: {}".format(name))
        else:
            value = default_value
            logger.debug("Using default {} value".format(name))
    elif value_type != str:
        value = value_type(value)
    logger.debug("{} = {}".format(name, value))
    return value


HAWKBIT_CONFIG = hawkbit.Config(
    server=__get_config_value('HAWKBIT_SERVER'),
    tenant=__get_config_value('HAWKBIT_TENANT'),
    device=__get_config_value('HAWKBIT_DEVICE'),
    token=__get_config_value('HAWKBIT_TOKEN'),
)

HONO_CONFIG = hono.Config(
    server=__get_config_value('HONO_SERVER'),
    username=__get_config_value('HONO_USERNAME'),
    password=__get_config_value('HONO_PASSWORD'),
)

if __missing_config_detected:
    exit(1)

hawkbit_client = hawkbit.Client(HAWKBIT_CONFIG)
hono_client = hono.Client(HONO_CONFIG, handle_config_changed=hawkbit_client.enqueue_check_config_command)

hono_client.start()
hawkbit_client.start()
