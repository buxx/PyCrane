from PyCrane.objects.AppObjects import AppObjects
from PyCrane.resource.ModelResource import ModelResource


class AppList(ModelResource):

    def _model_collection(self):
        return AppObjects(self._get_supervisor().get_apps())

    def get(self):
        apps = [app.to_dict() for app in self._objects.get_collection()]
        return self._core.get_response(apps)
