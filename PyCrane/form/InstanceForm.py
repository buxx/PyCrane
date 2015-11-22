from wtforms import StringField, validators, BooleanField

from PyCrane.form.Form import Form


class InstanceForm(Form):

    host = StringField('Host name')
    app = StringField('App model')
    image = StringField('Image name', validators=[validators.input_required()])
    enabled = BooleanField('Is working', validators=[validators.input_required()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        hosts_names = [host.get_name() for host in self._supervisor.get_hosts()]
        apps_images = [app.get_image() for app in self._supervisor.get_apps()]

        self.host.validators = [validators.input_required(),
                                validators.any_of(hosts_names)]
        self.image.validators = [validators.input_required(),
                                 validators.any_of(apps_images)]

