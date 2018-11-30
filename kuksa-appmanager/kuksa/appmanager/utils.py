# Copyright (c) 2018 Eclipse KUKSA project
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0
#
# SPDX-License-Identifier: EPL-2.0
#
# Contributors: Robert Bosch GmbH

import hashlib


class ConfigurationError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def md5(content):
    content_hash = hashlib.md5()
    content_hash.update(content)
    return content_hash.hexdigest()
