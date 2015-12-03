from PyCrane.exception import ConfigurationException


class Model:
    _dict_fields = []

    def __getattr__(self, name):
        if name[0:4] == 'get_':
            attr_name = '_' + name[4:]
            if hasattr(self, attr_name):
                return lambda: getattr(self, attr_name)
        if name[0:4] == 'set_':
            attr_name = '_' + name[4:]
            if hasattr(self, attr_name):
                return lambda value: setattr(self, attr_name, value)
        raise AttributeError("Unknown model attribute '%s'" % (str(name)))

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        if not self._dict_fields:
            raise ConfigurationException("No _dict_fields configured for '%s' model" % (str(self),))

        dict_data = {}
        for field, field_render_name in self._dict_fields:
            dict_data[field_render_name] = getattr(self, field)

        return dict_data
