from PyCrane.objects.host import HostObjects
from PyCrane.resource.base import ModelResource
from PyCrane.message import ResponseContent


class Host(ModelResource):
    def _model_collection(self):
        return HostObjects(self._get_supervisor().get_hosts())

    def _get_content(self, host_name):
        host = self._objects.find_one_by_name(host_name)
        return ResponseContent(host.to_dict())


class HostList(ModelResource):
    def _model_collection(self):
        return HostObjects(self._get_supervisor().get_hosts())

    def _get_content(self):
        return ResponseContent([host.to_dict() for host in self._objects.get_collection()])
