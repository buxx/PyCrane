from flask import Flask

from PyCrane.resource.Instances import Instances
from PyCrane.resource.tools import contextualise_resource
from PyCrane.server.Api import Api
from PyCrane.resource.AppList import AppList
from PyCrane.resource.App import App
from PyCrane.resource.HostList import HostList
from PyCrane.resource.Host import Host


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

    def _contextualise_resource(self, ressource_class):
        return contextualise_resource(ressource_class, self._supervisor)

    def _build_app_resources(self):
        self._api.add_resource(self._contextualise_resource(AppList), '/apps')
        self._api.add_resource(self._contextualise_resource(App), '/app/<app_name>')

    def _build_host_resources(self):
        self._api.add_resource(self._contextualise_resource(HostList), '/hosts')
        self._api.add_resource(self._contextualise_resource(Host), '/host/<host_name>')

        self._api.add_resource(self._contextualise_resource(Instances), '/instances')
        # GET: List configured images (and list errors of hosts don't have)
        # POST: sync hosts images (pull needed)
        #  self._api.add_resource(self._contextualise_resource(Images), '/images')

    def get_response(self, content: dict, http_code=200, request_errors=[]):
        return {
            'request': {
                'errors': request_errors
            },
            'response': content
        }, http_code

    def get_error_response(self, message, error_name='Error', http_code=400, content=''):
        request_errors = [{
            'name': error_name,
            'message': message
        }]
        return self.get_response(content, http_code, request_errors)
