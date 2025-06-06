from django import forms
from django.utils.translation import gettext as _

from apps.core.widgets import get_text_widget, get_textarea_widget

from .. import models


class GroupForm(forms.ModelForm):
    class Meta:
        model = models.Group
        fields = ("name", "kind", "description")
        widgets = {
            "name": get_text_widget(placeholder=_("e.g. Financial Department")),
            "description": get_textarea_widget(),
        }
