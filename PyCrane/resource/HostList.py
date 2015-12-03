from PyCrane.objects.HostObjects import HostObjects
from PyCrane.resource.ModelResource import ModelResource
from PyCrane.resource.message import ResponseContent


class HostList(ModelResource):

    def _model_collection(self):
        return HostObjects(self._get_supervisor().get_hosts())

    def _get_content(self):
        return ResponseContent([host.to_dict() for host in self._objects.get_collection()])
