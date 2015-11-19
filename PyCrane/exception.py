class PyCraneException(Exception):
    pass


class FatalException(PyCraneException):
    pass


class DisplayableException(PyCraneException):
    pass


class ConfigurationException(FatalException):
    pass


class NotFound(DisplayableException):
    pass
