from PyCrane.exception import ConfigurationException, NotFound


class Objects:

    _collection = None

    def get_collection(self) -> list:
        if self._collection is None:
            raise ConfigurationException("Subclass must set model object's")
        return self._collection

    def find_one_by_name(self, name: str):
        """
        TODO: Et si plusieurs avec mm name ?
        :param name:
        :return:
        """
        for obj in self.get_collection():
            if obj.get_name() == name:
                return obj

        raise NotFound("Can't find object for name '%s'" % (name,))
