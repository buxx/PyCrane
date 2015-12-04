from flask import Flask
from flask_restful import Api as ApiBase
from tinydb import TinyDB
from typing import List
from PyCrane.command.foreman import ComposeForeman, Foreman
from PyCrane.message import ResponseError
from PyCrane.model.app import App as AppModel
from PyCrane.model.host import Host as HostModel
from PyCrane.resource.app import AppList, App, Instances, Instance
from PyCrane.resource.base import contextualise_resource, Resource
from PyCrane.resource.host import HostList, Host


class Supervisor:
    """
    PyCrane manager class
    """
    def __init__(self, config: dict):
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

    def get_core(self):
        """
        :rtype: Core
        """
        return self._core

    @classmethod
    def get_foreman_class(cls) -> Foreman:
        """
        Return docker connector. Override here to use your own docker manipulation class
        """
        return ComposeForeman

    def start_server(self):
        """
        Start Flask server according to config
        """
        self._core.run(**self._config.get('server', {}))


class Api(ApiBase):
    """
    RESTFul api control: Manage available resources
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._supervisor = self.app.get_supervisor()  # type: Supervisor

    def build_resources(self):
        """
        Populate resources with apps, hosts, instances etc
        :return:
        """
        self._build_app_resources()
        self._build_host_resources()

    def _contextualise_resource(self, ressource_class) -> Resource:
        """
        Flask[REST] resources ae given as class, we encapsulate theses class here to give them
        supervisor instance at __init__
        :param ressource_class: Class of resource
        :return: Contextualised resource
        """
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
    """
    Flask main app
    """
    def __init__(self, supervisor, *args, **kwargs):
        super().__init__('PyCrane', *args, **kwargs)  # TODO: Conf import_name ?
        self._supervisor = supervisor
        self._api = Api(self)
        self._api.build_resources()

    def get_supervisor(self) -> Supervisor:
        return self._supervisor

    def get_response(self, content, http_code: int=200, request_errors: List[ResponseError]=[]):
        """
        Return standardised PyCrane response for REST messages
        :param content: the raw content of response, can be None, str, list, dict
        :param http_code: HTTP code of response
        :param request_errors: list of ResponseError to add in response
        :return:
        """
        return {
                   'request': {
                       'errors': [error.to_dict() for error in request_errors]
                   },
                   'response': content
               }, http_code

    def get_error_response(self, error: ResponseError, http_code: int=400, content=None):
        """
        Return an standardised PyCrane error response
        :param error: The ResponseError of response
        :param http_code: HTTP code of response
        :param content: the raw content of response, can be None, str, list, dict
        :return:
        """
        return self.get_response(content, http_code, [error])
