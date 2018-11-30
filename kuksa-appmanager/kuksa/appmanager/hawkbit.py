# Copyright (c) 2018 Eclipse KUKSA project
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0
#
# SPDX-License-Identifier: EPL-2.0
#
# Contributors: Robert Bosch GmbH

import json
import logging
import time
from queue import Queue
from threading import Lock
from threading import Thread

from requests import Session

from . import __version__
from .services import DockerSession
from .utils import ConfigurationError
from .utils import md5


class Config:
    def __init__(self, server: str, tenant: str, device: str, token: str):
        self.server = server
        self.tenant = tenant
        self.device = device
        self.token = token


class Client:
    CHECK_CONFIG_COMMAND = 'check-config'

    def __init__(self, config: Config):
        self.logger = logging.getLogger(self.__class__.__module__ + '.' + self.__class__.__name__)
        self.config = config
        self.poll_interval = 5 * 60  # 5 minutes
        self.active = True

        self.http = Session()
        self.http.headers.update({
            'Authorization': 'TargetToken {token}'.format(token=config.token),
        })

        self.deployment_job = None
        self.deployment_job_lock = Lock()

        self.queue = Queue()

        self.polling = True
        self.next_poll = 0

    def start(self):
        self.next_poll = time.time()

        def schedule_next_poll():
            while self.polling:
                if 0 < self.next_poll < time.time():
                    self.queue.put((Client.CHECK_CONFIG_COMMAND, 'scheduler'))

                time.sleep(1)  # 1 second

        Thread(name='HawkBitClientScheduler', daemon=True, target=schedule_next_poll).start()

        try:
            while self.active:
                command, source = self.queue.get(block=True)
                self.logger.debug("News '{}' command from '{}'".format(command, source))

                if command == Client.CHECK_CONFIG_COMMAND:
                    try:
                        self.next_poll = 0
                        self.__check_config()
                    finally:
                        self.next_poll = time.time() + self.poll_interval
                else:
                    raise Exception("Unsupported command: {}".format(command))
        finally:
            self.polling = False

    def enqueue_check_config_command(self, source):
        self.queue.put((Client.CHECK_CONFIG_COMMAND, source))

    def __check_config(self):
        actions = self.__request_actions()

        if actions:
            for action_name, action in actions.items():
                action_url = action.get('href')
                self.logger.debug("Handle '{}' action: {}".format(action_name, action_url))
                if action_name == 'deploymentBase':
                    self.__do_deployment_base(action_url)
                elif action_name == 'cancelAction':
                    self.__do_cancel_action(action_url)
                elif action_name == 'configData':
                    self.__do_config_data(action_url)
                else:
                    self.logger.error("Unsupported action: {}".format(action_name))
        else:
            self.logger.debug("No actions received")

    def __request_actions(self):
        actions_response = self.http.get(
            url='{server}/{tenant}/controller/v1/{controller_id}'.format(
                server=self.config.server,
                tenant=self.config.tenant,
                controller_id=self.config.device
            ),
            headers={
                'Accept': 'application/json'
            }
        )

        # TODO: handle response errors
        actions_response.raise_for_status()

        actions: dict = actions_response.json()
        self.logger.debug("Received actions: {}".format(actions))

        # update polling interval
        polling_sleep = actions.get('config', {}).get('polling', {}).get('sleep')
        if polling_sleep:
            hours, minutes, seconds = map(lambda s: int(s), polling_sleep.split(':'))
            self.poll_interval = hours * 3600 + minutes * 60 + seconds

        return actions.get('_links', {})

    def __do_cancel_action(self, action_url):
        action_response = self.http.get(
            url=action_url
        )

        # TODO: handle request errors
        action_response.raise_for_status()

        action = action_response.json()
        action_id = action['id']

        # stop ongoing deployment
        with self.deployment_job_lock:
            if self.deployment_job and self.deployment_job.active:
                if self.deployment_job.action_id == action_id:
                    self.deployment_job.cancel()
                else:
                    self.logger.warning("There is no deployment active with ID: {}".format(action.id))

        self._send_feedback(action_url, action_id, execution='closed', finished='success')

        # trigger a new configuration check because usually a cancel action is followed by a deploymentBase action...
        self.enqueue_check_config_command('cancellation')

    def __do_config_data(self, action_url):
        response = self.http.put(
            url=action_url,
            json=dict(
                mode='replace',
                data={
                    'clientVersion': __version__
                },
                status=dict(
                    execution='closed',
                    result=dict(
                        finished='success'
                    ),
                    details=[]
                )
            )
        )

        # TODO: handle request errors
        response.raise_for_status()

    def __do_deployment_base(self, action_url):
        action_url = action_url.split('?')[0]  # drop URL params

        with self.deployment_job_lock:
            create_deployment_job = True

            if self.deployment_job and self.deployment_job.active:
                if self.deployment_job.action_url == action_url:
                    create_deployment_job = False
                else:
                    self.deployment_job.cancel()

            if create_deployment_job:
                self.deployment_job = DeploymentJob(self, action_url)

    def _send_feedback(self, action_url, action_id, execution, finished):
        response = self.http.post(
            url='{}/feedback'.format(action_url),
            json=dict(
                id=action_id,
                status=dict(
                    result=dict(
                        finished=finished
                    ),
                    execution=execution
                )
            )
        )
        response.raise_for_status()


class DeploymentJob:
    def __init__(self, client: Client, action_url: str):
        self.logger = logging.getLogger(self.__class__.__module__ + '.' + self.__class__.__name__)
        self.client = client
        self.http = client.http
        self.action_id = action_url.split('/')[-1]
        self.action_url = action_url
        self.active = True
        self.cancelled = False

        self.thread = Thread(target=self.__run, daemon=True)
        self.thread.start()

    def cancel(self):
        self.cancelled = True
        self.thread.join()  # wait until the thread finishes

    def __run(self):
        try:
            self.__cancelled_check()

            deployment_response = self.http.get(self.action_url)
            deployment_response.raise_for_status()

            deployment = deployment_response.json()
            assert self.action_id == deployment['id']

            self.__cancelled_check()

            self.__send_feedback('proceeding', 'none')

            try:
                deployment_services = self.__get_services(deployment)

                with DockerSession(self.__cancelled_check) as docker:
                    docker.deploy(deployment_services)

                self.__send_feedback('closed', 'success')
            except ConfigurationError as error:
                self.logger.error(error)
                # TODO: forward error message to HawkBit
                self.__send_feedback('closed', 'failure')
        except self.__class__.CancelledException:
            self.logger.warning("Deployment {} was cancelled".format(self.action_id))
        except Exception as error:
            self.logger.exception(error)
        finally:
            self.active = False

    def __cancelled_check(self):
        if self.cancelled:
            raise self.__class__.CancelledException()

    class CancelledException(Exception):
        pass

    def __send_feedback(self, execution, finished):
        self.client._send_feedback(self.action_url, self.action_id, execution, finished)

    def __get_services(self, deployment):
        services = {}
        for chunk in deployment['deployment']['chunks']:
            service_name = chunk['name']
            self.logger.debug("Provisioning chunk: {name}".format(name=service_name))

            for artifact in chunk['artifacts']:
                self.__cancelled_check()

                self.logger.debug(artifact)
                artifact_filename = artifact['filename']
                if artifact_filename == 'docker-container.json':
                    artifact_response = self.http.get(artifact['_links']['download-http']['href'])
                    artifact_response.raise_for_status()

                    artifact_content = artifact_response.content
                    assert md5(artifact_content) == artifact['hashes']['md5']

                    if service_name in services:
                        # invalid configuration detected
                        raise ConfigurationError("Duplicate service configuration for service: {}".format(service_name))

                    service: dict = json.loads(artifact_content)
                    service.update(dict(
                        name=service_name,
                        version=chunk['version'],
                    ))

                    services[service_name] = service
                else:
                    self.logger.debug("Ignored artifact: {filename}".format(filename=artifact_filename))

            if service_name not in services:
                raise ConfigurationError("Missing 'docker-container.json' artifact for service: {}".format(service_name))

        return services
