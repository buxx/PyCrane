from tinydb import Query
from PyCrane.exception import NotFound

from PyCrane.model import Host
from PyCrane.model.Instance import Instance


class Instances:

    def __init__(self, database): # TODO: OpenClosed database
        """
        TODO: Etre coherent dans les retours: retourner des Instance, ou des dicts.
        :param database:
        :return:
        """
        self._database = database
        self._instances = Query()

    def get_all(self) -> list:
        return [Instance.from_dict(instance_data) for instance_data in self._database.all()]

    def find_by_host(self, host: Host) -> list:  # TODO: typehint [Instance]
        return [Instance.from_dict(data) for data in self._database.search(self._instances.host == host.get_name())]

    def create(self, data: dict):
        return self._database.insert(data)

    def find_one_by_name(self, name: str) -> Instance:
        search_results = self._database.search(self._instances.name == name)
        if not search_results:
            raise NotFound('No instance with name "{0}"'.format(name))
        return Instance.from_dict(search_results.pop())

    def update(self, instance: Instance):
        self._database.update(instance.to_dict(), self._instances.name == instance.get_name())

    def delete(self, instance: Instance):
        self._database.remove(self._instances.name == instance.get_name())
