from flask import Flask
from flask_restful import Api as ApiBase
from PyCrane.message import ResponseError
from PyCrane.resource.app import AppList, App, Instances, Instance
from PyCrane.resource.base import contextualise_resource
from PyCrane.resource.host import HostList, Host


class Api(ApiBase):
    """
    RESTFul api control.
    TODO: Ajout des URLs de gestion
     * des modèles d'Applications
     * des hotes
     * d'accès aux méthodes docker-py (avec server/hote param)
     * d'accès aux modules (ajout dynamique!) de gest. des contenairs (docker-compose)
    """
    pass


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
        self._api.add_resource(self._contextualise_resource(Instance), '/instance/<instance_name>')
        # GET: List configured images (and list errors of hosts don't have)
        # POST: sync hosts images (pull needed)
        #  self._api.add_resource(self._contextualise_resource(Images), '/images')

    def get_response(self, content: dict, http_code=200, request_errors=[]):
        return {
                   'request': {
                       'errors': [error.to_dict() for error in request_errors]
                   },
                   'response': content
               }, http_code

    def get_error_response(self, error: ResponseError, http_code=400, content=None):
        return self.get_response(content, http_code, [error])
