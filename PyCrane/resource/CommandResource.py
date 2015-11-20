from PyCrane.command.Command import Command
from PyCrane.objects.HostObjects import HostObjects
from PyCrane.resource.ModelResource import ModelResource


class CommandResource(ModelResource):

    def __init__(self, supervisor, *args, **kwargs):
        super().__init__(supervisor, *args, **kwargs)
        self._command = Command(self._objects.get_collection())

    def _model_collection(self):
        return HostObjects(self._get_supervisor().get_hosts())

    def _get_extend_hosts_command_result(self, command_name, parameters):
        result = []
        for host in self._objects.get_collection():
            result.extend(self._command.get_command_result(command_name, host, parameters))
        return result
