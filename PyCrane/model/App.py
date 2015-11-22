from PyCrane.model.Model import Model


class App(Model):

    _dict_fields = [('_name', 'name'),
                    ('_image', 'image')]

    def __init__(self, name, image):
        self._name = name
        self._image = image
