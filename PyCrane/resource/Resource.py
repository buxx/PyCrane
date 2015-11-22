from flask_restful import Resource as ResourceBase

from PyCrane.exception import ConfigurationException, NotFound, DisplayableException


class Resource(ResourceBase):
    """
    TODO: Si la resource enfant ne veut pas de post, put , etc: Lister dans ttr de classe et reproduire erreur
    comme si methode n'existait pas.
    """

    def get(self, *args, **kwargs):
        try:
            return self._core.get_response(self._get_content(*args, **kwargs))
        except NotFound as exc:
            return self._core.get_error_response(str(exc), 404)
        except DisplayableException as exc:
            return self._core.get_error_response(str(exc))

    def post(self, *args, **kwargs):
        try:
            return self._core.get_response(self._post_content(*args, **kwargs))
        except DisplayableException as exc:
            return self._core.get_error_response(str(exc))

    def put(self, *args, **kwargs):
        try:
            return self._core.get_response(self._put_content(*args, **kwargs))
        except DisplayableException as exc:
            return self._core.get_error_response(str(exc))

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
