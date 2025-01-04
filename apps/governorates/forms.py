from django import forms

from .models import Governorate


class GovernorateForm(forms.ModelForm):

    class Meta:
        model = Governorate
        fields = ("name", "description")