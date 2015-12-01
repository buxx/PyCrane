from PyCrane.model.Instance import Instance


class InstanceDispatcher:

    def __init__(self, supervisor, instance: Instance=None):
        self._before = {}
        if instance:
            self._before = instance.to_dict()
        self._foreman = supervisor.get_foreman_class()(supervisor)

    def dispatch(self, instance: Instance):
        if self._property_changed('enabled', instance):
            if instance.get_enabled():
                self._foreman.run(instance)
            else:
                self._foreman.stop(instance)

        return instance

    def _property_changed(self, property_name, instance: Instance):
        return self._before.get(property_name) is not getattr(instance, property_name)
