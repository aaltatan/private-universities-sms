from django import forms
from django.utils.translation import gettext as _

from apps.core.fields import get_autocomplete_field
from apps.core.widgets import (
    get_numeric_widget,
    get_text_widget,
    get_textarea_widget,
)

from . import models


class JobTypeForm(forms.ModelForm):
    class Meta:
        model = models.JobType
        fields = ("name", "description")
        widgets = {
            "name": get_text_widget(placeholder=_("job type name")),
            "description": get_textarea_widget(),
        }


class JobSubtypeForm(forms.ModelForm):
    job_type = get_autocomplete_field(
        queryset=models.JobType.objects.all(),
        to_field_name="name",
        widget_attributes={"placeholder": _("search job types")},
        app_label="org",
        model_name="JobType",
        object_name="jobtype",
        field_name="search",
    )

    class Meta:
        model = models.JobSubtype
        fields = ("name", "job_type", "description")
        widgets = {
            "name": get_text_widget(placeholder=_("job subtype name")),
            "description": get_textarea_widget(),
        }


class GroupForm(forms.ModelForm):
    class Meta:
        model = models.Group
        fields = ("name", "description")
        widgets = {
            "name": get_text_widget(placeholder=_("group name")),
            "description": get_textarea_widget(),
        }


class CostCenterForm(forms.ModelForm):
    class Meta:
        model = models.CostCenter
        fields = ("name", "accounting_id", "description")
        widgets = {
            "name": get_text_widget(placeholder=_("cost center name")),
            "accounting_id": get_numeric_widget(
                placeholder=_("cost center id"),
            ),
            "description": get_textarea_widget(),
        }


class PositionForm(forms.ModelForm):
    class Meta:
        model = models.Position
        fields = ("name", "order", "description")
        widgets = {
            "name": get_text_widget(placeholder=_("position name")),
            "order": get_numeric_widget(
                placeholder=_("position order"),
            ),
            "description": get_textarea_widget(),
        }


class StatusForm(forms.ModelForm):
    is_payable = forms.ChoiceField(
        choices=models.Status.PayableChoices,
        label=_("is payable"),
        help_text=_("is it payable or not"),
    )

    class Meta:
        model = models.Status
        fields = ("name", "is_payable", "description")
        widgets = {
            "name": get_text_widget(placeholder=_("status name")),
            "description": get_textarea_widget(),
        }


class DepartmentForm(forms.ModelForm):
    parent = get_autocomplete_field(
        queryset=models.Department.objects.all(),
        to_field_name="name",
        widget_attributes={"placeholder": _("search parents")},
        field_attributes={"required": False},
        app_label="org",
        model_name="Department",
        object_name="department",
        field_name="search",
    )
    cost_center = get_autocomplete_field(
        queryset=models.CostCenter.objects.all(),
        to_field_name="name",
        widget_attributes={"placeholder": _("search cost centers")},
        app_label="org",
        model_name="CostCenter",
        object_name="costcenter",
        field_name="search",
    )

    class Meta:
        model = models.Department
        fields = ("name", "parent", "cost_center", "description")
        widgets = {
            "name": get_text_widget(placeholder=_("job subtype name")),
            "description": get_textarea_widget(),
        }
