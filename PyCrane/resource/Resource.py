from flask_restful import Resource as ResourceBase

from PyCrane.exception import ConfigurationException, NotFound, DisplayableException
from PyCrane.resource.message import ResponseError


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

    def get(self, *args, **kwargs):
        return self._get_final_response('get', args, kwargs)

    def post(self, *args, **kwargs):
        return self._get_final_response('post', args, kwargs)

    def put(self, *args, **kwargs):
        return self._get_final_response('put', args, kwargs)

    def delete(self, *args, **kwargs):
        return self._get_final_response('delete', args, kwargs)

    def _get_final_response(self, method, args, kwargs):
        real_method_name = "_{0}_content".format(method)
        if not hasattr(self, real_method_name):
            response_error = ResponseError("Method not allowed",
                                           "The method is not allowed for the requested URL.")
            return self._core.get_error_response(response_error)
        method = getattr(self, real_method_name)

        try:
            resp = method(*args, **kwargs)
            return self._core.get_response(content=resp.get_content(),
                                           request_errors=resp.get_errors())
        except NotFound as exc:
            response_error = ResponseError('Not Found', str(exc))
            return self._core.get_error_response(response_error, 404)

        except DisplayableException as exc:
            response_error = ResponseError(exc.__class__.__name__, str(exc))
            return self._core.get_error_response(response_error, content=exc.get_response_content())
