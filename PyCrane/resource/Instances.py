from PyCrane.exception import InvalidPost
from PyCrane.form.InstanceForm import InstanceForm
from PyCrane.model.Instances import Instances as InstancesModel
from PyCrane.objects.HostObjects import HostObjects
from PyCrane.resource.CommandResource import CommandResource
from flask import request


class Instances(CommandResource):

    def __init__(self, supervisor, *args, **kwargs):
        super().__init__(supervisor, *args, **kwargs)
        self._instances = InstancesModel(supervisor.get_db())

    def _model_collection(self):
        return HostObjects(self._get_supervisor().get_hosts())

    def _get_content(self):
        return self._instances.get_all()

    def _post_content(self):
        instance_form = InstanceForm(request.form)
        if instance_form.validate():
            self._instances.create(instance_form.data)
        else:
            raise InvalidPost('Invalid data provided', response_content=instance_form.errors)

    def _put_content(self):
        # TODO: Les instances doivent avoir un ID (id container?)
        pass  # TODO
