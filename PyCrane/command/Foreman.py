from PyCrane.model.Instance import Instance
from PyCrane.objects.HostObjects import HostObjects
from PyCrane.objects.Instances import Instances


class Foreman:

    def __init__(self, supervisor):
        self._supervisor = supervisor
        self._hosts = HostObjects(supervisor.get_hosts())
        self._instances = Instances(supervisor.get_db())

    def run(self, instance: Instance):
        raise NotImplementedError()
