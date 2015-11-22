from PyCrane.model.Model import Model
from PyCrane.objects.AppObjects import AppObjects


class Instance(Model):

    _dict_fields = [('_host', 'host'),
                    ('_app', 'app'),
                    ('_enabled', 'enabled'),
                    ('_image', 'image')]

    @classmethod
    def get_apps_from_dict(cls, apps_dict: dict) -> []:  # TODO: Type d'objets ?
        apps = []
        for app_name in apps_dict:
            app_dict = apps_dict[app_name]
            apps.append(cls(name=app_name,
                            image=app_dict['image']))
        return apps

    def __init__(self, host, app, enabled, image):
        self._host = host
        self._app = app
        self._enabled = enabled
        self._image = image

    def _get_image_name_from_app(self, app_name):
        apps = AppObjects(self._get_supervisor().get_apps())
        return apps.find_one_by_name(app_name).get_image()
