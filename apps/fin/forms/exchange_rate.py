from decimal import Decimal

from django import forms
from django.utils.translation import gettext as _

from apps.core.widgets import (
    get_date_widget,
    get_money_widget,
    get_textarea_widget,
)

from .. import models


class ExchangeRateForm(forms.ModelForm):
    currency = forms.ModelChoiceField(
        queryset=models.Currency.objects.filter(is_primary=False),
        label=_("currency"),
    )
    rate = forms.DecimalField(
        label=_("rate"),
        widget=get_money_widget(decimal_places=8),
    )

    def clean(self):
        raw_rate: str = self.data["rate"]
        if raw_rate:
            raw_rate = Decimal(raw_rate.replace(",", ""))
            if "rate" in self.errors.as_data():
                rate_errors = [
                    error.message for error in self.errors.as_data().get("rate")
                ]
                if _("Enter a number.") in rate_errors:
                    self.errors.pop("rate")
                    return self.cleaned_data.update({"rate": raw_rate})

        return self.cleaned_data

    class Meta:
        model = models.ExchangeRate
        fields = ("currency", "date", "rate", "notes")
        widgets = {
            "date": get_date_widget(),
            "rate": get_money_widget(decimal_places=8),
            "notes": get_textarea_widget(),
        }
