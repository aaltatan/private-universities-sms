from django.utils.translation import gettext as _

from apps.core.fields import get_autocomplete_field
from apps.core.forms import CustomModelForm
from apps.core.widgets import get_date_widget, get_text_widget, get_textarea_widget
from apps.fin.models import Period, VoucherKind

from .. import models


class BaseVoucherForm(CustomModelForm):
    period = get_autocomplete_field(
        Period.objects.all(),
        to_field_name="name",
        widget_attributes={"placeholder": _("search periods")},
        app_label="fin",
        model_name="Period",
        object_name="period",
        field_name="search",
    )
    kind = get_autocomplete_field(
        VoucherKind.objects.all(),
        to_field_name="name",
        widget_attributes={"placeholder": _("search voucher kinds")},
        app_label="fin",
        model_name="VoucherKind",
        object_name="voucher_kind",
        field_name="search",
    )

    class Meta:
        model = models.Voucher
        fields = (
            "title",
            "date",
            "kind",
            "month",
            "quarter",
            "period",
            "serial_id",
            "serial_date",
            "approve_date",
            "due_date",
            "document",
            "notes",
        )
        widgets = {
            "title": get_text_widget(placeholder=_("e.g. January 2022 Salaries")),
            "date": get_date_widget(placeholder=_("e.g. 2022-01-05")),
            "serial_id": get_text_widget(placeholder=_("e.g. w/1234")),
            "serial_date": get_date_widget(
                placeholder=_("e.g. 2022-01-04"),
                fill_onfocus=False,
            ),
            "approve_date": get_date_widget(
                placeholder=_("e.g. 2022-01-03"),
                fill_onfocus=False,
            ),
            "due_date": get_date_widget(
                placeholder=_("e.g. 2022-01-10"),
                fill_onfocus=False,
            ),
            "notes": get_textarea_widget(placeholder=_("some notes")),
        }


class VoucherForm(BaseVoucherForm):
    pass
