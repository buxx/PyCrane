from flask import Flask
from PyCrane.server.Api import Api


class Core(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._api = Api(self)

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

    def _build_app_resources(self):
        # Class are loaded here because they needs Supervisor instantiation
        from PyCrane.resource.AppList import AppList
        from PyCrane.resource.App import App

        self._api.add_resource(App, '/app/<app_name>')
        self._api.add_resource(AppList, '/app')

    def _build_host_resources(self):
        # Class are loaded here because they needs Supervisor instantiation
        from PyCrane.resource.HostList import HostList
        from PyCrane.resource.Host import Host

        self._api.add_resource(Host, '/host/<host_name>')
        self._api.add_resource(HostList, '/host')

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
