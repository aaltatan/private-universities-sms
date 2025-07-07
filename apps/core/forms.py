from django import forms
from django.utils.translation import gettext as _

from apps.hr.models import Employee

from .fields import CustomModelChoiceField, get_autocomplete_field


class CustomModelForm(forms.ModelForm):
    """
    A custom ModelForm.

    This class is used to add autocomplete fields to the form.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if type(field) == CustomModelChoiceField:
                related_instance = getattr(self.instance, field_name, None)

                if self.instance and related_instance:
                    self.initial[field_name] = getattr(
                        related_instance, field.to_field_name
                    )


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
