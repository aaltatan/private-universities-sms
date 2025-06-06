from django import forms
from django.utils.translation import gettext as _

from apps.core.widgets import (
    get_numeric_widget,
    get_text_widget,
    get_textarea_widget,
)

from .. import models


class CostCenterForm(forms.ModelForm):
    class Meta:
        model = models.CostCenter
        fields = ("name", "accounting_id", "description")
        widgets = {
            "name": get_text_widget(placeholder=_("e.g. Architecture")),
            "accounting_id": get_numeric_widget(
                placeholder=_("cost center id"),
            ),
            "description": get_textarea_widget(),
        }
