from django import forms

from apps.core.widgets import (
    get_autocomplete_field,
    get_numeric_widget,
    get_textarea_widget,
)

from . import models


class JobTypeForm(forms.ModelForm):
    class Meta:
        model = models.JobType
        fields = ("name", "description")
        widgets = {
            "description": get_textarea_widget(),
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
            "description": get_textarea_widget(),
        }


class GroupForm(forms.ModelForm):
    class Meta:
        model = models.Group
        fields = ("name", "description")
        widgets = {
            "description": get_textarea_widget(),
        }


class CostCenterForm(forms.ModelForm):
    class Meta:
        model = models.CostCenter
        fields = ("name", "accounting_id", "description")
        widgets = {
            "accounting_id": get_numeric_widget(),
            "description": get_textarea_widget(),
        }
