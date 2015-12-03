from PyCrane.model.base import Model


class Host(Model):
    _dict_fields = [('_name', 'name'),
                    ('_hostname', 'hostname'),
                    ('_socket', 'socket')]

    def __init__(self, name, hostname, socket):
        self._name = name
        self._hostname = hostname
        self._socket = socket
