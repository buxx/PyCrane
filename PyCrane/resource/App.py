from PyCrane.objects.AppObjects import AppObjects
from PyCrane.resource.ModelResource import ModelResource
from PyCrane.resource.message import ResponseContent


class App(ModelResource):

    def _model_collection(self):
        return AppObjects(self._get_supervisor().get_apps())

    def _get_content(self, app_name):
        app = self._objects.find_one_by_name(app_name)
        return ResponseContent(app.to_dict())
