from PyCrane.objects.AppObjects import AppObjects
from PyCrane.exception import DisplayableException, NotFound
from PyCrane.resource.ModelResource import ModelResource


class App(ModelResource):

    def _model_collection(self):
        return AppObjects(self._get_supervisor().get_apps())

    def get(self, app_name):
        try:
            app = self._objects.find_one_by_name(app_name)
            return self._core.get_response(app.to_dict())
        except NotFound as exc:
            return self._core.get_error_response(str(exc), 404)
        except DisplayableException as exc:
            return self._core.get_error_response(str(exc))
