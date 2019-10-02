# Copyright (c) 2019 Eclipse KUKSA project
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0
#
# SPDX-License-Identifier: EPL-2.0
#
# Contributors: Paderborn University

import datetime
import json
import os


class AppRegistry:

    APP_REGISTRY_DIR = '/var/lib/kuksa-appmanager/'
    APP_REGISTRY_FILE = 'appregistry.json'

    def add_widget(self, id):
        registry = self.__openregistry()

        widget_details = dict()
        widget_details['id'] = id
        widget_details['type'] = 'widget'
        widget_details['installdate'] = datetime.datetime.utcnow().isoformat()

        registry.append(widget_details)
        self.__saveregistry(registry)

    def remove_widget(self, id):
        registry = self.__openregistry()
        registry = [widget for widget in registry if widget['id'] != id]
        self.__saveregistry(registry)

    def installed_widgets(self):
        registry = self.__openregistry()
        return registry

    def __openregistry(self):
        if os.path.isfile(self.APP_REGISTRY_DIR + self.APP_REGISTRY_FILE):
            with open(self.APP_REGISTRY_DIR + self.APP_REGISTRY_FILE) as json_file:
                return json.load(json_file)
        else:
            # No registry file exists yet
            return []

    def __saveregistry(self, registry):
        # Make sure directory exists
        if not os.path.exists(self.APP_REGISTRY_DIR):
            os.makedirs(self.APP_REGISTRY_DIR)

        with open(self.APP_REGISTRY_DIR + self.APP_REGISTRY_FILE, 'w') as json_file:
            json.dump(registry, json_file)