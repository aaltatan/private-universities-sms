from django import forms
from django.utils.translation import gettext_lazy as _

from apps.core.forms import CustomModelForm
from apps.core.widgets import get_text_widget, get_textarea_widget

from .. import models


class StatusForm(CustomModelForm):
    is_payable = forms.ChoiceField(
        choices=models.Status.PayableChoices,
        label=_("is payable"),
    )
    is_separated = forms.ChoiceField(
        choices=models.Status.SeparatedChoices,
        label=_("is separated"),
    )

    class Meta:
        model = models.Status
        fields = ("name", "is_payable", "is_separated", "description")
        widgets = {
            "name": get_text_widget(placeholder=_("e.g. Active")),
            "description": get_textarea_widget(placeholder=_("some description")),
        }
