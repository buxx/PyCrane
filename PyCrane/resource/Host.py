from PyCrane.objects.HostObjects import HostObjects
from PyCrane.exception import DisplayableException
from PyCrane.resource.Resource import Resource


class Host(Resource):

    _objects = HostObjects()

    def get(self, host_name):
        try:
            host = self._objects.find_one_by_name(host_name)
            return self._core.get_response(host.to_dict())
        except DisplayableException as exc:
            # TODO: catch la bonne erreur, NotFound, puis Displayable (recup err?)
            return self._core.get_404_response(str(exc))
