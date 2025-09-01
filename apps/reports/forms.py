from django import forms
from django.utils.translation import gettext_lazy as _

from apps.core.fields import get_autocomplete_field
from apps.hr.models import Employee


class LedgerForm(forms.Form):
    employee = get_autocomplete_field(
        Employee.objects.all(),
        to_field_name="slug",
        widget_attributes={"placeholder": _("search employees")},
        app_label="hr",
        model_name="Employee",
        object_name="employee",
        field_name="search",
    )

    class Meta:
        model = Employee
        fields = ["employee"]
