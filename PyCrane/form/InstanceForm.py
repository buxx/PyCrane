from wtforms import StringField, validators, BooleanField, ValidationError
from PyCrane.exception import NotFound

from PyCrane.form.Form import Form
from PyCrane.objects.Instances import Instances


class InstanceForm(Form):

    name = StringField('Instance name', validators=[validators.input_required()])
    host = StringField('Host name')
    app = StringField('App model')
    image = StringField('Image name', validators=[validators.input_required()])
    enabled = BooleanField('Is working', validators=[validators.input_required()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._instances = Instances(self._supervisor.get_db())

        hosts_names = [host.get_name() for host in self._supervisor.get_hosts()]
        apps_images = [app.get_image() for app in self._supervisor.get_apps()]

        self.host.validators = [validators.input_required(),
                                validators.any_of(hosts_names)]
        self.image.validators = [validators.input_required(),
                                 validators.any_of(apps_images)]
    @staticmethod
    def validate_name(form, field):
        try:
            if form._instances.find_one_by_name(field.data):  # Better way (protected attribute usage) ?
                raise ValidationError('{0} already exist'.format(field.data))
        except NotFound:
            pass  # name is valid if no instance

