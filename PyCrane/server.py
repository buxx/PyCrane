from flask import Flask
from flask_restful import Api as ApiBase
from tinydb import TinyDB
from typing import List
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
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._supervisor = self.app.get_supervisor()  # type: Supervisor

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
        self.add_resource(self._contextualise_resource(AppList), '/apps')
        self.add_resource(self._contextualise_resource(App), '/app/<app_name>')

    def _build_host_resources(self):
        self.add_resource(self._contextualise_resource(HostList), '/hosts')
        self.add_resource(self._contextualise_resource(Host), '/host/<host_name>')

        self.add_resource(self._contextualise_resource(Instances), '/instances')
        self.add_resource(self._contextualise_resource(Instance), '/instance/<instance_name>')


class Core(Flask):
    def __init__(self, supervisor, *args, **kwargs):
        super().__init__('PyCrane', *args, **kwargs)  # TODO: Conf import_name ?
        self._supervisor = supervisor
        self._api = Api(self)
        self._api.build_resources()

    def get_supervisor(self):
        return self._supervisor

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
        self._config = config

    def get_db(self, db_name='db') -> TinyDB:
        db_file_name = "{0}/{1}.json".format(self._config.get('db_path', './'), db_name)
        return TinyDB(db_file_name)

    def get_apps(self) -> List[AppModel]:
        return self._apps

    def get_hosts(self) -> List[HostModel]:
        return self._hosts

    def get_core(self) -> Core:
        return self._core

    @classmethod
    def get_foreman_class(cls):
        return ComposeForeman

    def start_server(self):
        # TODO: parametres hos etc en argv
        self._core.run(host='127.0.0.1', port=5000, debug=True)