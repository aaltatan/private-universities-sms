from django import forms

from apps.core.widgets import get_email_widget

from .. import models


class EmailForm(forms.ModelForm):
    class Meta:
        model = models.Email
        fields = ("email", "kind")
        widgets = {
            "email": get_email_widget(),
        }
