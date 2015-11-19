from PyCrane.objects.HostObjects import HostObjects
from PyCrane.resource.Resource import Resource


class HostList(Resource):

    _objects = HostObjects()

    def get(self):
        hosts = [host.to_dict() for host in self._objects.get_collection()]
        return self._core.get_response(hosts)
