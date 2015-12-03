from PyCrane.model.base import Model


class App(Model):
    _dict_fields = [('_name', 'name'),
                    ('_image', 'image'),
                    ('_command', 'command')]

    def __init__(self, name, image, command=None):
        self._name = name
        self._image = image
        self._command = command


class Instance(Model):
    _dict_fields = [('_name', 'name'),
                    ('_host', 'host'),
                    ('_app', 'app'),
                    ('_enabled', 'enabled'),
                    ('_image', 'image'),
                    ('_command', 'command')]

    def __init__(self, host, app, enabled, image, name, command=None):
        self._host = host
        self._app = app
        self._enabled = enabled
        self._image = image
        self._name = name
        self._command = command

    @property
    def enabled(self):
        return self._enabled

    def get_enabled(self):
        """
        TODO: c'est sale ça :
        :return:
        """
        if self._enabled in ['1', 1, True]:
            return True
        if self._enabled in ['0', 0, False]:
            return False
