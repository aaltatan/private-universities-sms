from django.utils.translation import gettext as _

from apps.core.fields import get_autocomplete_field
from apps.core.forms import CustomModelForm
from apps.core.widgets import get_textarea_widget, get_number_widget
from apps.fin.models import Compensation
from apps.hr.models import Employee

from .. import models


class BaseVoucherTransactionForm(CustomModelForm):
    employee = get_autocomplete_field(
        Employee.objects.all(),
        to_field_name="firstname",
        widget_attributes={"placeholder": _("search employees")},
        app_label="hr",
        model_name="Employee",
        object_name="employee",
        field_name="search",
    )
    compensation = get_autocomplete_field(
        Compensation.objects.all(),
        to_field_name="name",
        widget_attributes={"placeholder": _("search compensations")},
        app_label="fin",
        model_name="Compensation",
        object_name="compensation",
        field_name="search",
    )

    class Meta:
        model = models.VoucherTransaction
        fields = (
            "employee",
            "compensation",
            "quantity",
            "value",
            "notes",
        )
        widgets = {
            "quantity": get_number_widget(placeholder=_("e.g. 1")),
            "value": get_number_widget(placeholder=_("e.g. 1000")),
            "notes": get_textarea_widget(placeholder=_("some notes")),
        }


class VoucherTransactionForm(BaseVoucherTransactionForm):
    pass
