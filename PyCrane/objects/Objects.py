from PyCrane.exception import NotFound


class Objects:

    def __init__(self, collection):
        self._collection = collection

    def find_one_by_name(self, name: str):
        """
        TODO: Et si plusieurs avec mm name ?
        :param name:
        :return:
        """
        for obj in self._collection:
            if obj.get_name() == name:
                return obj

        raise NotFound("Can't find object for name '%s'" % (name,))
