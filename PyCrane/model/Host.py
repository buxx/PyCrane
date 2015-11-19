from PyCrane.model.Model import Model


class Host(Model):

    _dict_fields = [('_name', 'name'),
                    ('_hostname', 'hostname'),
                    ('_socket', 'socket')]

    @classmethod
    def get_hosts_from_dict(cls, hosts_dict: dict) -> []:  # TODO: Type d'objets ?
        """
        TODO: Automatiser dans Model
        :param hosts_dict:
        :return:
        """
        hosts = []
        for host_name in hosts_dict:
            host_dict = hosts_dict[host_name]
            hosts.append(cls(name=host_name,
                             hostname=host_dict['hostname'],

                             socket=host_dict['socket']))
        return hosts

    def __init__(self, name, hostname, socket):
        self._name = name
        self._hostname = hostname
        self._socket = socket
