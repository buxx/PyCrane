from PyCrane.objects.HostObjects import HostObjects
from PyCrane.resource.ModelResource import ModelResource


class HostList(ModelResource):

    def _model_collection(self):
        return HostObjects(self._get_supervisor().get_hosts())

    def _get_content(self):
        return [host.to_dict() for host in self._objects.get_collection()]
