from django import forms
from django.utils.translation import gettext as _

from apps.core.widgets import get_text_widget, get_textarea_widget

from .. import models


class BaseYearForm(forms.ModelForm):
    class Meta:
        model = models.Year
        fields = ("name", "description")
        widgets = {
            "name": get_text_widget(placeholder=_("e.g. 2022")),
            "description": get_textarea_widget(),
        }


class YearForm(BaseYearForm):
    pass
