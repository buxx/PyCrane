from PyCrane.command.InstanceDispatcher import InstanceDispatcher
from PyCrane.objects.HostObjects import HostObjects
from PyCrane.resource.CommandResource import CommandResource
from PyCrane.objects.Instances import Instances as InstancesObjects


class InstanceBase(CommandResource):

    def __init__(self, supervisor, *args, **kwargs):
        super().__init__(supervisor, *args, **kwargs)
        self._instances = InstancesObjects(supervisor.get_db())

    def _model_collection(self):
        return HostObjects(self._get_supervisor().get_hosts())

    def _get_dispatcher(self, instance=None):
        """

        :param instance: Instance object if already exist
        :return:
        """
        return InstanceDispatcher(self._supervisor, instance)
