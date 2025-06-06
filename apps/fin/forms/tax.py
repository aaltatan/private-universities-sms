from django import forms
from django.utils.translation import gettext as _

from apps.core.widgets import get_text_widget, get_textarea_widget

from .. import models


class BaseTaxForm(forms.ModelForm):
    fixed = forms.ChoiceField(
        choices=models.Tax.FixedChoices,
        label=_("fixed"),
    )

    class Meta:
        model = models.Tax
        fields = (
            "name",
            "fixed",
            "rate",
            "rounded_to",
            "round_method",
            "description",
        )
        widgets = {
            "name": get_text_widget(placeholder=_("e.g. Fixed Tax")),
            "rate": get_text_widget(placeholder=_("e.g. 0.1")),
            "rounded_to": get_text_widget(placeholder=_("e.g. 100")),
            "description": get_textarea_widget(),
        }


class TaxForm(BaseTaxForm):
    pass
