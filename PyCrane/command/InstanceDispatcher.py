from PyCrane.command.Command import Command
from PyCrane.exception import StartedBecauseShouldBeRunning
from PyCrane.model.Instance import Instance
from PyCrane.objects.HostObjects import HostObjects


class InstanceDispatcher:
    def __init__(self, supervisor, instance: Instance = None):
        self._before = {}
        if instance:
            self._before = instance.to_dict()
        self._foreman = supervisor.get_foreman_class()(supervisor)
        self._command = Command(HostObjects(supervisor.get_hosts()))

    def dispatch(self, instance: Instance):
        if instance.get_enabled():
            instance_running = self._command.is_running(instance)
            just_enabled = self._property_changed('enabled', instance)

            if just_enabled or not instance_running:
                self._foreman.run(instance)

            if not just_enabled and not instance_running:
                raise StartedBecauseShouldBeRunning(
                    "Instance {0} started because not running on {1}".format(instance.get_name(),
                                                                             instance.get_host()))
        else:
            self._foreman.stop(instance)

        return instance

    def _property_changed(self, property_name, instance: Instance):
        return self._before.get(property_name) is not getattr(instance, property_name)
