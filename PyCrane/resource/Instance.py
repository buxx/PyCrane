from PyCrane.resource.InstanceBase import InstanceBase
from flask import request


class Instance(InstanceBase):

    def _put_content(self, instance_name):
        instance = self._instances.find_one_by_name(instance_name)
        dispatcher = self._get_dispatcher(instance)

        for attr_name in request.form.keys():
            getattr(instance, 'set_%s' % attr_name)(request.form.get(attr_name))

        self._instances.update(instance)
        dispatcher.dispatch(instance)

        return instance.to_dict()

    def _delete_content(self, instance_name):
        instance = self._instances.find_one_by_name(instance_name)
        dispatcher = self._get_dispatcher(instance)
        instance.set_enabled(False)
        dispatcher.dispatch(instance)
        self._instances.delete(instance)
