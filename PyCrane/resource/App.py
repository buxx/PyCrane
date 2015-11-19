from PyCrane.objects.AppObjects import AppObjects
from PyCrane.exception import DisplayableException
from PyCrane.resource.Resource import Resource


class App(Resource):

    _objects = AppObjects()

    def get(self, app_name):
        try:
            app = self._objects.find_one_by_name(app_name)
            return self._core.get_response(app.to_dict())
        except DisplayableException as exc:
            # TODO: catch la bonne erreur, NotFound, puis Displayable (recup err?)
            return self._core.get_404_response(str(exc))
