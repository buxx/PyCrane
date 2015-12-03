from docker import Client
from PyCrane.exception import AlreadyRunning
from PyCrane.model import Instance


class Command:
    """

    NOTE: THIS CLASS IS NOT FINISHED AND CAN BE DELETED

    """

    def __init__(self, hosts):
        self._hosts = hosts
        self._clients = {}

    def _get_client(self, host):
        host_name = host.get_name()
        if host_name not in self._clients:
            self._clients[host_name] = Client(base_url=host.get_socket())
        return self._clients[host_name]

    def get_command_result(self, command_name, host, parameters):
        client = self._get_client(host)
        return getattr(client, command_name)(**parameters)

    def run(self, instance: Instance):
        if self.exist(instance):
            if self.is_running(instance):
                raise AlreadyRunning()
            self.start(instance)
        else:
            self.create(instance)
            self.run(instance)

    def exist(self, instance: Instance):
        instance_name = instance.get_name()
        if not instance_name:
            return False
        host = self._hosts.find_one_by_name(instance.get_host())
        return self._container_exist(host, instance.get_name())

    def _container_exist(self, host, name, parameters={}):
        client = self._get_client(host)
        # TODO: Refact et regler le probleme de filters
        containers = client.containers(all=True, **parameters)  # TODO: filters= bug ?!
        for container in containers:
            container_names = container.get('Names')
            if name in container_names or '/' + name in container_names:
                return True
        return False

    def is_running(self, instance: Instance):
        host = self._hosts.find_one_by_name(instance.get_host())
        return self._container_exist(host, instance.get_name(), {'filters': {'status': 'running'}})

    def start(self, instance: Instance):
        pass

    def create(self, instance: Instance):
        pass

    def image_available(self, image_name, host):
        pass

    def pull(self, image_name, host):
        pass