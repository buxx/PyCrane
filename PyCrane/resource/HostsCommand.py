from flask_restful import reqparse
from PyCrane.command.Command import Command
from PyCrane.model.Host import Host
from PyCrane.objects.HostObjects import HostObjects
from PyCrane.exception import DisplayableException, NotFound
from PyCrane.resource.ModelResource import ModelResource


class HostsCommand(ModelResource):
    """
    TODO: Toutes les commandes ne peuvent pas être lancès sur la grappe d'host
    --> il faut preciser l'hote pour certaines (create, start ?) OU PAS si on fiat genre cluster
    """

    def __init__(self, supervisor, *args, **kwargs):
        super().__init__(supervisor, *args, **kwargs)
        self._command = Command(self._objects.get_collection())

    def _model_collection(self):
        return HostObjects(self._get_supervisor().get_hosts())

    def get(self, command_name: str) -> dict:
        try:
            parameters = {}  # TODO: recuperer les params
            command_result = self._command.get_command_result(command_name, parameters)
            return self._core.get_response(command_result)
        except DisplayableException as exc:
            return self._core.get_error_response(str(exc))
