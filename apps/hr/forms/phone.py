from django import forms
from django.utils.translation import gettext as _

from apps.core.widgets import get_numeric_widget

from .. import models


class PhoneForm(forms.ModelForm):
    class Meta:
        model = models.Phone
        fields = ("number", "kind")
        widgets = {
            "number": get_numeric_widget(
                placeholder=_("phone number"),
            ),
        }
