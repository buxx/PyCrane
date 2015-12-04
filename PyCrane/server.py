from flask import Flask
from flask_restful import Api as ApiBase
from tinydb import TinyDB
from PyCrane.command.foreman import ComposeForeman
from PyCrane.message import ResponseError
from PyCrane.model.app import App as AppModel
from PyCrane.model.host import Host as HostModel
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


class Supervisor:
    def __init__(self, config: dict):
        """

        :param config: dict config TODO: link to doc
        :return:
        """
        self._apps = [AppModel.from_dict(app_data) for app_data in config['APPS']]
        self._hosts = [HostModel.from_dict(host_data) for host_data in config['HOSTS']]
        self._core = Core(self)
        self._core.build_resources()
        self._db = self._get_database(config)
        self._config = config

    def _get_database(self, config):
        return TinyDB('./db.json')  # TODO: config

    def set_apps(self, apps: list):  # TODO: type dans liste
        self._apps = apps

    def get_apps(self) -> list:  # TODO: type dans liste
        return self._apps

    def set_hosts(self, hosts: list):  # TODO: type dans liste
        self._hosts = hosts

    def get_hosts(self) -> list:  # TODO: type dans liste
        return self._hosts

    def get_core(self):
        return self._core

    def get_db(self) -> TinyDB:
        return self._db

    def get_foreman_class(self):
        return ComposeForeman

    def start_server(self):
        # TODO: parametres hos etc en argv
        self._core.run(host='127.0.0.1', port=5000, debug=True)