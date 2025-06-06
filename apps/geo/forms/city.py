from django import forms
from django.utils.translation import gettext as _

from apps.core.widgets import get_text_widget, get_textarea_widget

from .. import models


class BaseCityForm(forms.ModelForm):
    class Meta:
        model = models.City
        fields = ("name", "governorate", "kind", "description")
        widgets = {
            "name": get_text_widget(placeholder=_("e.g. Hamah")),
            "description": get_textarea_widget(),
        }


class CityForm(BaseCityForm):
    pass
