from PyCrane.objects.HostObjects import HostObjects
from PyCrane.exception import DisplayableException, NotFound
from PyCrane.resource.Resource import Resource


class Host(Resource):

    _objects = HostObjects()

    def get(self, host_name):
        try:
            host = self._objects.find_one_by_name(host_name)
            return self._core.get_response(host.to_dict())
        except NotFound as exc:
            return self._core.get_error_response(str(exc), 404)
        except DisplayableException as exc:
            return self._core.get_error_response(str(exc))
