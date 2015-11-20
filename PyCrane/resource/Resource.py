from flask_restful import Resource as ResourceBase
from PyCrane.exception import ConfigurationException


class Resource(ResourceBase):

    def __init__(self, supervisor, *args, **kwargs):
        super(*args, **kwargs)
        self._supervisor = supervisor
        self._core = supervisor.get_core()

    def _get_supervisor(self):
        """
        TODO: doc ! (fournis lors de la contextualisation)
        :return: Supervisor
        """
        if self._supervisor is None:
            raise ConfigurationException("_supervisor must be set")
        return self._supervisor
