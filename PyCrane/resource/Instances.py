from flask import request
from werkzeug.datastructures import MultiDict
from PyCrane.exception import InvalidPost
from PyCrane.form.InstanceForm import InstanceForm
from PyCrane.model.Instance import Instance
from PyCrane.objects.AppObjects import AppObjects
from PyCrane.resource.InstanceBase import InstanceBase
from PyCrane.resource.message import ResponseContent


class Instances(InstanceBase):

    _inherited_fields = ('image', 'command')

    def _get_content(self):
        instances_data = [instance.to_dict() for instance in self._instances.get_all()]
        instances_errors = self._get_instances_errors(self._instances.get_all())
        return ResponseContent(instances_data, instances_errors)

    def _post_content(self):
        request_data = self._complete_request_data(request.form)
        instance_form = InstanceForm(request_data, supervisor=self._get_supervisor())
        dispatcher = self._get_dispatcher(None)

        if instance_form.validate():
            instance = Instance.from_dict(instance_form.data)
            self._instances.create(instance.to_dict())  # TODO: Donner Instance plutôt qur dict ?
            dispatcher.dispatch(instance)
            return ResponseContent(instance.to_dict())
        else:
            raise InvalidPost('Invalid data provided', response_content=instance_form.errors)

    def _complete_request_data(self, request_data) -> MultiDict:
        """
        Replace 'image' by model app image name if not set
        :param request_data: dict of request.data (or equivalent)
        :return: MultiDict
        """
        request_data = dict(request_data)
        request_data = self._complete_request_inherited(request_data)
        return MultiDict(request_data)

    def _complete_request_inherited(self, request_data: dict):
        if not request_data.get('app'):
            return

        instance_app_name = request_data.get('app')[0]
        apps = AppObjects(self._get_supervisor().get_apps())
        app = apps.find_one_by_name(instance_app_name)

        for inherited_field_name in self._inherited_fields:
            if not request_data.get(inherited_field_name):
                inherited_value = getattr(app, "get_{0}".format(inherited_field_name))()
                request_data[inherited_field_name] = [inherited_value]

        return request_data
