from PyCrane.objects.Objects import Objects
from PyCrane.resource.Resource import Resource


class ModelResource(Resource):

    def __init__(self, supervisor, *args, **kwargs):
        super().__init__(supervisor, *args, **kwargs)
        self._objects = self._model_collection()

    def _model_collection(self) -> Objects:
        raise NotImplementedError()
