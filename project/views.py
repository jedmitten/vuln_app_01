from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm


class SecureModelView(ModelView):
    form_base_class = SecureForm
