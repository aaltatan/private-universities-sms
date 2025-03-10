from django import forms
from django.utils.translation import gettext as _

from apps.core.widgets import (
    get_numeric_widget,
    get_text_widget,
    get_textarea_widget,
)

from .. import models


class PositionForm(forms.ModelForm):
    class Meta:
        model = models.Position
        fields = ("name", "order", "description")
        widgets = {
            "name": get_text_widget(placeholder=_("position name")),
            "order": get_numeric_widget(
                placeholder=_("position order"),
            ),
            "description": get_textarea_widget(),
        }
