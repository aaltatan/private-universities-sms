from django import forms
from django.utils.translation import gettext as _

from apps.core.forms import CustomModelForm
from apps.core.widgets import get_text_widget, get_textarea_widget

from .. import models


class NationalityForm(CustomModelForm):
    is_local = forms.ChoiceField(
        choices=models.Nationality.LocalityChoices,
        label=_("locality"),
    )

    class Meta:
        model = models.Nationality
        fields = ("name", "is_local", "description")
        widgets = {
            "name": get_text_widget(placeholder=_("e.g. Syrian")),
            "description": get_textarea_widget(),
        }
