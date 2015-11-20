from tinydb import Query


class Instances:

    def __init__(self, database):
        self._database = database

    def find_by_host(self, host):
        instances = Query()
        return self._database.search(instances.host == host.get_name())