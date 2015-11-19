from PyCrane.Supervisor import Supervisor
from PyCrane.objects.Objects import Objects


class AppObjects(Objects):
    _collection = Supervisor.get_instance().get_apps()
