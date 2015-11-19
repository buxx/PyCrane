from PyCrane.Supervisor import Supervisor
from PyCrane.objects.Objects import Objects


class HostObjects(Objects):
    _collection = Supervisor.get_instance().get_hosts()
