from django import forms
from django.utils.translation import gettext as _

from apps.core.widgets import get_text_widget, get_textarea_widget, get_date_widget

from .. import models


class BaseVoucherForm(forms.ModelForm):
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
