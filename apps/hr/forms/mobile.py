from django import forms
from django.utils.translation import gettext as _

from apps.core.widgets import get_numeric_widget

from .. import models


class MobileForm(forms.ModelForm):
    has_whatsapp = forms.ChoiceField(
        choices=models.Mobile.HasWhatsappChoices,
        label=_("has whatsapp"),
    )

    class Meta:
        model = models.Mobile
        fields = ("number", "has_whatsapp", "kind")
        widgets = {
            "number": get_numeric_widget(
                placeholder=_("mobile number"),
            ),
        }
