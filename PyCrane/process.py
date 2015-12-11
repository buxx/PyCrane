class Instanciate:

    def __init__(self, supervisor, app, instance, request_data):
        self._supervisor = supervisor
        self._app = app
        self._instance = instance
        self._request_data = request_data

    def update_instance(self, instance):
        pass

    def success(self):
        pass

    def fail(self):
        pass
