from tinydb import Query
from PyCrane.exception import NotFound, DisplayableException
from PyCrane.model.Instances import Instances
from PyCrane.objects.HostObjects import HostObjects
from PyCrane.resource.CommandResource import CommandResource


class HostInstances(CommandResource):

    def __init__(self, supervisor, *args, **kwargs):
        super().__init__(supervisor, *args, **kwargs)
        self._instances = Instances(supervisor.get_db())

    def _model_collection(self):
        return HostObjects(self._get_supervisor().get_hosts())

    def _get_content(self, host_name):
        host = self._objects.find_one_by_name(host_name)
        db_instances = self._instances.find_by_host(host)

        # TODO: check pour celle qui doivent être en marche si en marche
        return db_instances
