from PyCrane.objects.AppObjects import AppObjects
from PyCrane.resource.Resource import Resource


class AppList(Resource):

    _objects = AppObjects()

    def get(self):
        apps = [app.to_dict() for app in self._objects.get_collection()]
        return self._core.get_response(apps)
