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
        # TODO: host resources,
        # /host/<host_name
        # /host/<host_name>/containers
        #  etc

    def _build_app_resources(self):
        from PyCrane.resource.AppList import AppList
        from PyCrane.resource.App import App

        self._api.add_resource(App, '/app/<app_name>')
        self._api.add_resource(AppList, '/app')

    def get_response(self, content: dict, code=200, request_errors=[]):
        server_errors = self._get_server_errors()
        return {
            'request': {
                'errors': request_errors
            },
            'server': {
                'errors': server_errors
            },
            'content': content
        }, code

    def get_404_response(self, message):
        request_errors = [{'message': message}]
        return self.get_response('', 404, request_errors)

    def _get_server_errors(self):
        """
        TODO: do
        :return:
        """
        return []
