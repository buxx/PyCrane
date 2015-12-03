class ResponseContent:

    def __init__(self, content, errors=[]):
        self._content = content
        self._errors = errors

    def get_content(self):
        return self._content

    def get_errors(self):
        return self._errors


class ResponseError:

    def __init__(self, name, message, content=None):
        self._name = name
        self._message = message
        self._content = content

    def to_dict(self):
        return {
            'name': self._name,
            'message': self._message,
            'content': self._content
        }
