from PyCrane.exception import ConfigurationException
from PyCrane.app.App import App
from PyCrane.host.Host import Host


class Supervisor:

    _instance = None  # type: Supervisor
    """
    Used to Supervisor singleton
    """

    @classmethod
    def create_instance(cls, core, config: dict, supervisor_class: None):
        if cls._instance is not None:
            raise ConfigurationException("Singleton instance already created")

        if not supervisor_class:
            supervisor_class = cls

        cls._instance = supervisor_class(core, config)
        return cls._instance

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            raise ConfigurationException("Supervisor singleton not instanced")
        return cls._instance

    def __init__(self, core, config: dict):
        """

        :param core: Core PyCrane Core
        :param config: dict config TODO: link to doc
        :return:
        """
        self._apps = App.get_apps_from_dict(config['APPS'])
        self._hosts = Host.get_hosts_from_dict(config['HOSTS'])
        self._core = core

    def build(self):
        """

        :return:
        """
        self._core.build_resources()

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

    def start_server(self):
        # TODO: parametres hos etc en argv
        self._core.run(host='127.0.0.1', port=5000, debug=True)
