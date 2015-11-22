from wtforms import Form as FormBase


class Form(FormBase):

    def __init__(self, *args, supervisor, **kwargs):
        super().__init__(*args, **kwargs)
        self._supervisor = supervisor
