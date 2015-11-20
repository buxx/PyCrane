from PyCrane.objects.HostObjects import HostObjects
from PyCrane.exception import DisplayableException, NotFound
from PyCrane.resource.ModelResource import ModelResource


class Host(ModelResource):

    def _model_collection(self):
        return HostObjects(self._get_supervisor().get_hosts())

    def _get_content(self, host_name):
        host = self._objects.find_one_by_name(host_name)
        return host.to_dict()
