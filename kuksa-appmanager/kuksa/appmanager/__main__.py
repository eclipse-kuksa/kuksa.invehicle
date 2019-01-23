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
from .utils import ConfigurationError

logging.basicConfig(format='%(asctime)s - %(threadName)s - %(levelname)s - %(name)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger('kuksa.appmanager')


def __get_config_value(name):
    value = os.getenv(name)
    if not value:
        raise ConfigurationError("Missing environment variable: {}".format(name))
    return value


try:
    HAWKBIT_CONFIG = hawkbit.Config(
        server=__get_config_value('HAWKBIT_SERVER'),
        tenant=__get_config_value('HAWKBIT_TENANT'),
        device=__get_config_value('HAWKBIT_DEVICE'),
        token=__get_config_value('HAWKBIT_TOKEN'),
    )
except ConfigurationError as error:
    logger.error(error)
    exit(1)

try:
    HONO_CONFIG = hono.Config(
        server=__get_config_value('HONO_SERVER'),
        username=__get_config_value('HONO_USERNAME'),
        password=__get_config_value('HONO_PASSWORD'),
    )
except ConfigurationError as error:
    logger.warning(error)
    logger.warning("Hono feature is disabled")
    HONO_CONFIG = None

hawkbit_client = hawkbit.Client(HAWKBIT_CONFIG)

if HONO_CONFIG:
    hono_client = hono.Client(HONO_CONFIG, handle_config_changed=hawkbit_client.enqueue_check_config_command)
    hono_client.start()

hawkbit_client.start()
