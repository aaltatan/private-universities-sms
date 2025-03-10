from django import forms
from django.utils.translation import gettext as _

from apps.core.widgets import get_text_widget, get_textarea_widget

from .. import models


class StatusForm(forms.ModelForm):
    is_payable = forms.ChoiceField(
        choices=models.Status.PayableChoices,
        label=_("is payable"),
        help_text=_("is it payable or not"),
    )

    class Meta:
        model = models.Status
        fields = ("name", "is_payable", "description")
        widgets = {
            "name": get_text_widget(placeholder=_("status name")),
            "description": get_textarea_widget(),
        }
