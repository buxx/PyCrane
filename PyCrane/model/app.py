from PyCrane.model.base import Model
from PyCrane.process import Instanciate


class App(Model):
    _dict_fields = [('_name', 'name'),
                    ('_image', 'image'),
                    ('_command', 'command')]

    def __init__(self, name, image, command=None, instanciate=Instanciate):
        self._name = name
        self._image = image
        self._command = command
        self._instanciate = instanciate


class Instance(Model):
    _dict_fields = [('_name', 'name'),
                    ('_host', 'host'),
                    ('_app', 'app'),
                    ('_enabled', 'enabled'),
                    ('_image', 'image'),
                    ('_command', 'command'),
                    ('_volumes', 'volumes'),
                    ('_ports', 'ports')]

    def __init__(self, host, app, enabled, image, name, command=None, volumes=None, ports=None):
        self._host = host
        self._app = app
        self._enabled = enabled
        self._image = image
        self._name = name
        self._command = command
        self._volumes = volumes
        self._ports = ports

    @property
    def enabled(self):
        return self.get_enabled()

    def get_enabled(self):
        """
        TODO: c'est sale ça :
        :return:
        """
        if self._enabled in ['1', 1, True]:
            return True
        if self._enabled in ['0', 0, False]:
            return False
