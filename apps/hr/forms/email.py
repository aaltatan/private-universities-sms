from apps.core.forms import CustomModelForm
from apps.core.widgets import get_email_widget

from .. import models


class EmailForm(CustomModelForm):
    class Meta:
        model = models.Email
        fields = ("email", "kind")
        widgets = {
            "email": get_email_widget(),
        }
