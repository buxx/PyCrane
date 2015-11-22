from wtforms import Form, StringField, validators, BooleanField


class InstanceForm(Form):

    host = StringField('Host name', validators=[validators.input_required()])
    image = StringField('Image name', validators=[validators.input_required()])
    must_work = BooleanField('Is working', validators=[validators.input_required()])
