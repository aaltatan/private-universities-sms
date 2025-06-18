from django import forms
from django.utils.translation import gettext as _

from apps.core import widgets
from apps.core.forms import CustomModelForm

from .. import models


class BaseTaxBracketForm(CustomModelForm):
    tax = forms.ModelChoiceField(
        queryset=models.Tax.objects.filter(fixed=False),
        label=_("tax"),
    )

    class Meta:
        model = models.TaxBracket
        fields = (
            "tax",
            "amount_from",
            "amount_to",
            "rate",
            "notes",
        )
        widgets = {
            "amount_from": widgets.get_number_widget(placeholder=_("e.g. 1000")),
            "amount_to": widgets.get_number_widget(placeholder=_("e.g. 50000")),
            "rate": widgets.get_number_widget(placeholder=_("e.g. 0.1")),
            "notes": widgets.get_textarea_widget(),
        }


class TaxBracketForm(BaseTaxBracketForm):
    pass
