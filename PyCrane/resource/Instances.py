from flask import request
from werkzeug.datastructures import MultiDict

from PyCrane.exception import InvalidPost
from PyCrane.form.InstanceForm import InstanceForm
from PyCrane.objects.AppObjects import AppObjects
from PyCrane.objects.Instances import Instances as InstancesModel
from PyCrane.objects.HostObjects import HostObjects
from PyCrane.resource.CommandResource import CommandResource


class Instances(CommandResource):

    def __init__(self, supervisor, *args, **kwargs):
        super().__init__(supervisor, *args, **kwargs)
        self._instances = InstancesModel(supervisor.get_db())

    def _model_collection(self):
        return HostObjects(self._get_supervisor().get_hosts())

    def _get_content(self):
        return [instance.to_dict() for instance in self._instances.get_all()]

    def _post_content(self):
        request_data = self._complete_request_data(request.form)
        instance_form = InstanceForm(request_data, supervisor=self._get_supervisor())

        if instance_form.validate():
            self._instances.create(instance_form.data)
            # TODO: Une fois un id donne, retourné l'enregistrement ajouté
        else:
            raise InvalidPost('Invalid data provided', response_content=instance_form.errors)

    def _complete_request_data(self, request_data):
        """
        Replace 'image' by model app image name if not set
        :param request_data: dict of request.data (or equivalent)
        :return:
        """
        request_data = dict(request_data)
        if not request_data.get('image') and request_data.get('app'):
            apps = AppObjects(self._get_supervisor().get_apps())
            instance_app_name = request_data.get('app')[0]
            instance_image_name = apps.find_one_by_name(instance_app_name).get_image()
            request_data['image'] = [instance_image_name]

        return MultiDict(request_data)

    def _put_content(self):
        # TODO: Les instances doivent avoir un ID (id container?)
        pass  # TODO

    def _delete_content(self):
        # TODO: Les instances doivent avoir un ID (id container?)
        pass  # TODO
