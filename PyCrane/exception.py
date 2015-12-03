class PyCraneException(Exception):
    pass


class FatalException(PyCraneException):
    pass


class DisplayableException(PyCraneException):

    def __init__(self, *args, response_content=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._response_content = response_content

    def get_response_content(self):
        return self._response_content


class ConfigurationException(FatalException):
    pass


class NotFound(DisplayableException):
    pass


class InvalidPost(DisplayableException):
    pass


class NonFatalDisplayableException(DisplayableException):
    pass


class FatalDisplayableException(DisplayableException):
    pass


class AlreadyRunning(NonFatalDisplayableException):
    pass


class StartedBecauseShouldBeRunning(NonFatalDisplayableException):
    pass
