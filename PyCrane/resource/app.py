from flask import request
from werkzeug.datastructures import MultiDict
from PyCrane.command.dispatch import InstanceDispatcher

from PyCrane.exception import NonFatalDisplayableException, InvalidPost
from PyCrane.form.model import InstanceForm
from PyCrane.model.app import Instance as InstanceModel
from PyCrane.objects.apps import Apps
from PyCrane.objects.host import HostObjects
from PyCrane.process import Instanciate
from PyCrane.resource.base import ModelResource
from PyCrane.message import ResponseContent, ResponseError
from PyCrane.resource.command import CommandResource
from PyCrane.objects.apps import Instances as InstancesObjects
from PyCrane.model.app import App as AppModel


class App(ModelResource):
    def _model_collection(self):
        return Apps(self._get_supervisor().get_apps())

    def _get_content(self, app_name):
        app = self._objects.find_one_by_name(app_name)
        return ResponseContent(app.to_dict())


class AppList(ModelResource):
    def _model_collection(self):
        return Apps(self._get_supervisor().get_apps())

    def _get_content(self):
        return ResponseContent([app.to_dict() for app in self._objects.get_collection()])


class InstanceBase(CommandResource):
    def __init__(self, supervisor, *args, **kwargs):
        super().__init__(supervisor, *args, **kwargs)
        self._instances = InstancesObjects(supervisor.get_db())

    def _model_collection(self):
        return HostObjects(self._get_supervisor().get_hosts())

    def _get_dispatcher(self, instance=None):
        """

        :param instance: Instance object if already exist
        :return:
        """
        return InstanceDispatcher(self._supervisor, instance)

    def _get_instances_errors(self, instances):
        errors = []
        for instance in instances:
            if not self._command.is_running(instance):
                not_running_error = ResponseError('Instance not running',
                                                  "Instance {0} is not running".format(instance.get_name()),
                                                  instance.get_name())
                errors.append(not_running_error)
        return errors


class Instance(InstanceBase):
    def _put_content(self, instance_name):
        instance = self._instances.find_one_by_name(instance_name)
        dispatcher = self._get_dispatcher(instance)
        errors = []

        for attr_name in request.form.keys():
            getattr(instance, 'set_%s' % attr_name)(request.form.get(attr_name))

        self._instances.update(instance)

        try:
            dispatcher.dispatch(instance)
        except NonFatalDisplayableException as exc:
            errors.append(ResponseError('Forced start instance',
                                        str(exc)))

        return ResponseContent(None, errors=errors)

    def _delete_content(self, instance_name):
        instance = self._instances.find_one_by_name(instance_name)
        dispatcher = self._get_dispatcher(instance)
        instance.set_enabled(False)
        dispatcher.dispatch(instance)
        self._instances.delete(instance)
        return ResponseContent(None)


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
            instance = InstanceModel.from_dict(instance_form.data)
            instanciate = self._instanciate(instance, request_data)
            self._instances.create(instance.to_dict())  # TODO: Donner Instance plutôt qur dict ?
            try:
                dispatcher.dispatch(instance)
                instanciate.success()
            except Exception:  # TODO: Aller mettre des raise dans .dispatch
                instanciate.fail()
                raise
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
        apps = Apps(self._get_supervisor().get_apps())
        app = apps.find_one_by_name(instance_app_name)

        for inherited_field_name in self._inherited_fields:
            if not request_data.get(inherited_field_name):
                inherited_value = getattr(app, "get_{0}".format(inherited_field_name))()
                request_data[inherited_field_name] = [inherited_value]

        return request_data

    def _instanciate(self, instance, request_data) -> Instanciate:
        if not instance.get_app():
            return

        apps = Apps(self._get_supervisor().get_apps())
        app = apps.find_one_by_name(instance.get_app())

        instanciate = app.get_instanciate()(self._supervisor, app, instance, request_data)
        instanciate.update_instance(instance)
        return instanciate
