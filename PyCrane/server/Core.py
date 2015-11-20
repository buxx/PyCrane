from flask import Flask

from PyCrane.resource.tools import contextualise_resource
from PyCrane.server.Api import Api
from PyCrane.resource.AppList import AppList
from PyCrane.resource.App import App
from PyCrane.resource.HostList import HostList
from PyCrane.resource.Host import Host
from PyCrane.resource.HostCommand import HostCommand


class Core(Flask):

    def __init__(self, supervisor, *args, **kwargs):
        super().__init__('PyCrane', *args, **kwargs)  # TODO: Conf import_name ?
        self._api = Api(self)
        self._supervisor = supervisor

    def build_resources(self):
        """
        Populate ressources with apps, hosts, instances, docker-py, compose/...
        :return:
        """
        self._build_app_resources()
        self._build_host_resources()
        # TODO: host resources,
        # /host/<host_name
        # /host/<host_name>/containers
        #  etc

    def _contextualise_resource(self, ressource_class):
        return contextualise_resource(ressource_class, self._supervisor)

    def _build_app_resources(self):
        self._api.add_resource(self._contextualise_resource(AppList), '/app')
        self._api.add_resource(self._contextualise_resource(App), '/app/<app_name>')

    def _build_host_resources(self):
        self._api.add_resource(self._contextualise_resource(HostList), '/host')
        self._api.add_resource(self._contextualise_resource(Host), '/host/<host_name>')
        self._api.add_resource(self._contextualise_resource(HostCommand), '/host/<host_name>/<command_name>')

    def get_response(self, content: dict, code=200, request_errors=[]):
        server_errors = self._get_server_errors()
        return {
            'request': {
                'errors': request_errors
            },
            'server': {
                'errors': server_errors
            },
            'response': content
        }, code

    def get_error_response(self, message, code=500):
        request_errors = [{'message': message}]
        return self.get_response('', code, request_errors)

    def _get_server_errors(self):
        """
        TODO: do
        :return:
        """
        return []
