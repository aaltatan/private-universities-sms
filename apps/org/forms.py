from django import forms

from . import models


class JobTypeForm(forms.ModelForm):
    class Meta:
        model = models.JobType
        fields = ("name", "description")
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": 1,
                    "x-autosize": "",
                }
            ),
        }