from django.utils.translation import gettext as _

from apps.core.widgets import get_text_widget, get_textarea_widget
from apps.core.forms import CustomModelForm

from .. import models


class JobTypeForm(CustomModelForm):
    class Meta:
        model = models.JobType
        fields = ("name", "description")
        widgets = {
            "name": get_text_widget(placeholder=_("e.g. Software Developer")),
            "description": get_textarea_widget(),
        }
