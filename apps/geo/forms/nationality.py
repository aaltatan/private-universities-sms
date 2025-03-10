from django import forms
from django.utils.translation import gettext as _

from apps.core.widgets import get_text_widget, get_textarea_widget

from .. import models


class NationalityForm(forms.ModelForm):
    is_local = forms.ChoiceField(
        choices=models.Nationality.LocalityChoices,
        label=_("locality"),
        help_text=_("is it local or foreign"),
    )

    class Meta:
        model = models.Nationality
        fields = ("name", "is_local", "description")
        widgets = {
            "name": get_text_widget(placeholder=_("nationality name")),
            "description": get_textarea_widget(),
        }
