# Copyright (c) 2019 Eclipse KUKSA project
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0
#
# SPDX-License-Identifier: EPL-2.0
#
# Contributors: Paderborn University

import json
import logging
import subprocess

from .appregistry import AppRegistry
from .utils import ConfigurationError


class WidgetManager:

    def __init__(self):
        self.appregistry = AppRegistry()
        self.logger = logging.getLogger(self.__class__.__module__ + '.' + self.__class__.__name__)

    def deploy_widgets(self, deployment_widgets):

        self.undeploy_all_widgets()

        for widget in deployment_widgets:
            # Install widget with afm-util
            with subprocess.Popen(['afm-util', 'install', widget['path']], stdout=subprocess.PIPE) as install_widget_call:
                install_widget_call.wait()
                if install_widget_call.returncode != 0:
                    raise ConfigurationError("Widget {name} could not be installed".format(name=widget['path']))

                # Parse afm-util output to get widget id
                out, err = install_widget_call.communicate()
                out_json = json.loads(out.decode('utf-8'))
                widget_id = out_json['added']

                self.appregistry.add_widget(widget_id)
                self.logger.debug("Installed widget {}".format(widget_id))

    def undeploy_all_widgets(self):
        self.logger.debug("Undeploying all widgets")

        for widget in self.appregistry.installed_widgets():
            self.__undeploy_widget(widget['id'])

    def __undeploy_widget(self, widget_id):
        # Uninstall widget with afm-util
        with subprocess.Popen(['afm-util', 'uninstall', widget_id], stdout=subprocess.PIPE) as install_widget_call:
            install_widget_call.wait()
            if install_widget_call.returncode != 0:
                self.logger.warning("Uninstall failed: Widget {name} probably did not exist".format(name=widget_id))

            self.appregistry.remove_widget(widget_id)
