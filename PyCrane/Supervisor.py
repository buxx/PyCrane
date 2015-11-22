from tinydb import TinyDB
from PyCrane.model.App import App
from PyCrane.model.Host import Host
from PyCrane.server.Core import Core


class Supervisor:

    def __init__(self, config: dict):
        """

        :param config: dict config TODO: link to doc
        :return:
        """
        self._apps = [App.from_dict(app_data) for app_data in config['APPS']]
        self._hosts = [Host.from_dict(host_data) for host_data in config['HOSTS']]
        self._core = Core(self)
        self._core.build_resources()
        self._db = self._get_database(config)

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

    def start_server(self):
        # TODO: parametres hos etc en argv
        self._core.run(host='127.0.0.1', port=5000, debug=True)
