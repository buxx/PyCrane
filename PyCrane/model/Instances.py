from tinydb import Query
from PyCrane.model import Host


class Instances:

    def __init__(self, database): # TODO: OpenClosed database
        self._database = database
        self._instances = Query()

    def get_all(self) -> dict:
        return self._database.all()

    def find_by_host(self, host: Host) -> dict:
        return self._database.search(self._instances.host == host.get_name())

    def create(self, data: dict):
        self._database.insert(data)
