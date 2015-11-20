from PyCrane.objects.HostObjects import HostObjects
from PyCrane.resource.ModelResource import ModelResource


class HostList(ModelResource):

    def _model_collection(self):
        return HostObjects(self._get_supervisor().get_hosts())

    def get(self):
        hosts = [host.to_dict() for host in self._objects.get_collection()]
        return self._core.get_response(hosts)
