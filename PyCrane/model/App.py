from PyCrane.model.Model import Model


class App(Model):

    _dict_fields = [('_name', 'name'),
                    ('_image', 'image'),
                    ('_command', 'command')]

    def __init__(self, name, image, command=None):
        self._name = name
        self._image = image
        self._command = command
