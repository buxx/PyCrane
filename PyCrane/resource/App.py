from PyCrane.objects.AppObjects import AppObjects
from PyCrane.exception import DisplayableException, NotFound
from PyCrane.resource.ModelResource import ModelResource


class App(ModelResource):

    def _model_collection(self):
        return AppObjects(self._get_supervisor().get_apps())

    def _get_content(self, app_name):
        app = self._objects.find_one_by_name(app_name)
        return app.to_dict()
