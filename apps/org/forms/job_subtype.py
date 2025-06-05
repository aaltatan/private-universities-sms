from django import forms
from django.utils.translation import gettext as _

from apps.core.widgets import get_text_widget, get_textarea_widget

from .. import models


class BaseJobSubtypeForm(forms.ModelForm):
    class Meta:
        model = models.JobSubtype
        fields = ("name", "job_type", "description")
        widgets = {
            "name": get_text_widget(placeholder=_("job subtype name")),
            "description": get_textarea_widget(),
        }


class JobSubtypeForm(BaseJobSubtypeForm):
    pass
