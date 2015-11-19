from PyCrane.model.Model import Model


class App(Model):

    _dict_fields = [('_name', 'name'),
                    ('_image', 'image')]

    @classmethod
    def get_apps_from_dict(cls, apps_dict: dict) -> []:  # TODO: Type d'objets ?
        apps = []
        for app_name in apps_dict:
            app_dict = apps_dict[app_name]
            apps.append(cls(name=app_name,
                            image=app_dict['image']))
        return apps

    def __init__(self, name, image):
        self._name = name
        self._image = image
