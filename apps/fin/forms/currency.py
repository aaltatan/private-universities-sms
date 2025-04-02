from django import forms
from django.utils.translation import gettext as _

from apps.core.widgets import get_text_widget, get_textarea_widget

from .. import models


class CurrencyForm(forms.ModelForm):
    class Meta:
        model = models.Currency
        fields = (
            "name",
            "symbol",
            "code",
            "fraction_name",
            "decimal_places",
            "description",
        )
        widgets = {
            "name": get_text_widget(placeholder=_("currency name")),
            "symbol": get_text_widget(placeholder=_("symbol")),
            "code": get_text_widget(placeholder=_("code")),
            "fraction_name": get_text_widget(
                placeholder=_("fraction name"),
            ),
            "description": get_textarea_widget(),
        }
