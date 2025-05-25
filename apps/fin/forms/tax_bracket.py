from django import forms
from django.utils.translation import gettext as _

from apps.core.widgets import get_textarea_widget

from .. import models


class BaseTaxBracketForm(forms.ModelForm):

    tax = forms.ModelChoiceField(
        queryset=models.Tax.objects.filter(fixed=False),
        label=_("tax"),
        help_text=_("tax"),
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
            "notes": get_textarea_widget(),
        }


class TaxBracketForm(BaseTaxBracketForm):
    pass
