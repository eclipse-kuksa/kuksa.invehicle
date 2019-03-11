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
import os
from collections import OrderedDict
from typing import Callable

import docker
from docker.errors import ImageNotFound

from .utils import ConfigurationError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

DEPLOYMENTS_DIR = os.path.join(os.getcwd(), 'deployments')


class DockerSession:
    __DEPLOYED_SERVICES = 'services.json'
    __DEPLOYING_SERVICES = 'deploying_services.json'

    def __init__(self, cancelled_check: Callable[[], None]):
        self.docker: docker.DockerClient = None
        self.cancelled_check: Callable[[], None] = cancelled_check

    def __enter__(self):
        self.docker = docker.from_env()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.docker.close()

    def deploy(self, services: dict):
        assert services

        self.__prepare_deployment(services)

        services = self.__sort_services(services)

        self.__update_docker_images(services)

        self.__stop_and_remove_existing_services()

        try:
            self.__start_services(services)

            self.__commit_deployment()
        except Exception as error:
            self.__revert()

            raise error

    def undeploy_all_services(self):
        self.__stop_and_remove_existing_services()

    def __revert(self):
        try:
            with open(os.path.join(DEPLOYMENTS_DIR, self.__class__.__DEPLOYED_SERVICES), 'r') as fp:
                services = json.load(fp)
        except FileNotFoundError:
            services = {}

        services = self.__sort_services(services, cancellable=False)
        self.__stop_and_remove_existing_services(cancellable=False)
        self.__start_services(services)

    def __prepare_deployment(self, services: dict):
        try:
            os.mkdir(DEPLOYMENTS_DIR)
        except FileExistsError:
            pass

        with open(os.path.join(DEPLOYMENTS_DIR, self.__class__.__DEPLOYING_SERVICES), 'w') as fp:
            json.dump(services, fp, indent=True)

    def __commit_deployment(self):
        os.rename(os.path.join(DEPLOYMENTS_DIR, self.__class__.__DEPLOYING_SERVICES), os.path.join(DEPLOYMENTS_DIR, self.__class__.__DEPLOYED_SERVICES))

    def __sort_services(self, unsorted_services: dict, cancellable=True):
        if cancellable:
            self.cancelled_check()

        sorted_services = OrderedDict()

        while unsorted_services:
            unsorted_services_old_size = len(unsorted_services)
            for service_name, service in unsorted_services.items():
                service_dependencies: list = service.get('dependencies')
                if not service_dependencies:
                    # move this to the sorted devices
                    sorted_services[service_name] = service
                    del unsorted_services[service_name]

                    # remove this service from the dependencies list of all remaining services
                    for remaining_service in unsorted_services.values():
                        remaining_service_dependencies = remaining_service.get('dependencies') or []
                        if service_name in remaining_service_dependencies:
                            remaining_service_dependencies.remove(service_name)

                    # repeat process
                    break

            unsorted_services_new_size = len(unsorted_services)
            if unsorted_services_new_size == unsorted_services_old_size:
                # invalid configuration detected
                raise ConfigurationError(
                    "Service configuration problem detected for: {0}".format(', '.join(unsorted_services.keys()))
                )

        return sorted_services

    def __update_docker_images(self, services, cancellable=True):
        for service_name, service in services.items():
            if cancellable:
                self.cancelled_check()

            service_image_tarball = service.get('image-tarball')
            if service_image_tarball:
                # load image from downloaded file
                with open(service_image_tarball, 'rb') as __file:
                    self.docker.images.load(__file)
            else:
                service_image = service['image']
                auth_config = service.get('auths')
                logger.debug("Pulling docker image '{}' for service {}".format(service_image, service_name))
                try:
                    self.docker.images.pull(service_image, auth_config=auth_config)
                except docker.errors.ImageNotFound:
                    raise ConfigurationError("Docker image does not exist: {}".format(service_image))
                logger.debug("Finished pulling docker image '{}'".format(service_image))

    def __stop_and_remove_existing_services(self, cancellable=True):
        if cancellable:
            self.cancelled_check()

        containers = self.docker.containers.list(all=True, filters=dict(label='kuksa.appmanager.service=yes'))
        containers.sort(key=lambda c: int(c.labels.get('kuksa.appmanager.service.index')) or -1, reverse=True)
        for container in containers:
            service_version = container.labels.get('kuksa.appmanager.service.version')
            logger.info("Stopping service: {name}:{version}".format(name=container.name, version=service_version))
            container.remove(force=True)

    def __start_services(self, services):
        for index, (name, service) in enumerate(services.items()):
            container_params = dict(service.get('config') or {})

            container_params.update(dict(
                name=name,
                labels={
                    'kuksa.appmanager.service': 'yes',
                    'kuksa.appmanager.service.version': service['version'],
                    'kuksa.appmanager.service.index': str(index),
                },
                auto_remove=False,
                restart_policy={
                    'Name': 'unless-stopped',
                },
                detach=True,
            ))

            logger.info("Starting service: {name}:{version}".format(name=name, version=service['version']))
            logger.info("Params: {params}".format(params=container_params))
            try:
                self.docker.containers.run(service['image'], **container_params)
            except (docker.errors.DockerException, TypeError) as error:
                logger.exception(error)
                raise ConfigurationError("Failed to start the '{service_name}' service: {error}".format(service_name=name, error=error))
