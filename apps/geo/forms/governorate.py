from django import forms
from django.utils.translation import gettext as _

from apps.core.widgets import get_text_widget, get_textarea_widget

from .. import models


class GovernorateForm(forms.ModelForm):
    class Meta:
        model = models.Governorate
        fields = ("name", "description")
        widgets = {
            "name": get_text_widget(placeholder=_("governorate name")),
            "description": get_textarea_widget(),
        }
