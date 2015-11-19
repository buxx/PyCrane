from flask_restful import Resource as ResourceBase
from PyCrane.Supervisor import Supervisor


class Resource(ResourceBase):

    def __init__(self, *args, **kwargs):
        super(*args, **kwargs)
        self._core = Supervisor.get_instance().get_core()
