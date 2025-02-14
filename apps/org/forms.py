from django import forms

from apps.core.widgets import get_autocomplete_field

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


class JobSubtypeForm(forms.ModelForm):
    job_type = get_autocomplete_field(
        queryset=models.JobType.objects.all(),
        to_field_name="name",
        app_label="org",
        model_name="JobType",
        object_name="jobtype",
        field_name="search",
    )

    class Meta:
        model = models.JobSubtype
        fields = ("name", "job_type", "description")
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": 1,
                    "x-autosize": "",
                }
            ),
        }


class GroupForm(forms.ModelForm):
    class Meta:
        model = models.Group
        fields = ("name", "description")
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": 1,
                    "x-autosize": "",
                }
            ),
        }