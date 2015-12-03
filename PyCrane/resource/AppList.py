from PyCrane.objects.AppObjects import AppObjects
from PyCrane.resource.ModelResource import ModelResource
from PyCrane.resource.message import ResponseContent


class AppList(ModelResource):

    def _model_collection(self):
        return AppObjects(self._get_supervisor().get_apps())

    def _get_content(self):
        return ResponseContent([app.to_dict() for app in self._objects.get_collection()])
