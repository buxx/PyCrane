from PyCrane.command.Command import Command
from PyCrane.model.Host import Host
from PyCrane.objects.HostObjects import HostObjects
from PyCrane.exception import DisplayableException, NotFound
from PyCrane.resource.ModelResource import ModelResource


class HostCommand(ModelResource):
    """
    TODO: lister les actions (docker-py) qui sont dispo en GET, POST, etc ?
    et ne les autoriser que selon mode
    """

    def __init__(self, supervisor, *args, **kwargs):
        super().__init__(supervisor, *args, **kwargs)
        self._command = Command(self._objects)

    def _model_collection(self):
        return HostObjects(self._get_supervisor().get_hosts())

    def _get_host(self, host_name: str) -> Host:
        return self._objects.find_one_by_name(host_name)

    def get(self, host_name: str, command_name: str) -> dict:
        try:
            host = self._objects.find_one_by_name(host_name)
            parameters = {}  # TODO: recuperer les params
            command_result = self._command.get_command_result(command_name, parameters, host)
            return self._core.get_response(command_result)
        except NotFound as exc:
            return self._core.get_error_response(str(exc), 404)
        except DisplayableException as exc:
            return self._core.get_error_response(str(exc))
