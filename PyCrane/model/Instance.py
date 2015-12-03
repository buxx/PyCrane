from PyCrane.model.Model import Model
from PyCrane.objects.AppObjects import AppObjects


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

    def _get_image_name_from_app(self, app_name):
        apps = AppObjects(self._get_supervisor().get_apps())
        return apps.find_one_by_name(app_name).get_image()

    def get_enabled(self):
        """
        TODO: c'est sale ça :
        :return:
        """
        if self._enabled in ['1', 1, True]:
            return True
        if self._enabled in ['0', 0, False]:
            return False
