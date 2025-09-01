import openpyxl
from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from apps.core.fields import get_autocomplete_field
from apps.core.forms import BehaviorForm, CustomModelForm
from apps.core.validators import xlsx_extension_validator
from apps.core.widgets import (
    get_date_widget,
    get_file_widget,
    get_input_datalist_widget,
    get_text_widget,
    get_textarea_widget,
)
from apps.fin.models import Compensation, Period, VoucherKind
from apps.hr.models import Employee

from .. import models


class VoucherTransactionsImportForm(forms.Form):
    slug = forms.CharField(required=True)
    file = forms.FileField(
        widget=get_file_widget(),
        required=True,
        validators=[xlsx_extension_validator],
    )

    def save(self):
        file: InMemoryUploadedFile = self.cleaned_data.get("file")
        wb = openpyxl.load_workbook(file)
        voucher = get_object_or_404(
            models.Voucher,
            slug=self.cleaned_data.get("slug"),
        )
        for idx, row in enumerate(wb["data"]):
            if idx == 0:
                continue

            _, uuid, compensation_name, quantity, value, notes = [
                cell.value for cell in row
            ]

            employee = get_object_or_404(Employee, uuid=uuid)
            compensation = get_object_or_404(
                Compensation,
                name=compensation_name,
            )

            trans = models.VoucherTransaction(
                voucher=voucher,
                employee=employee,
                compensation=compensation,
                quantity=quantity,
                value=value,
                notes=notes if notes else "",
            )

            trans.save()


class AccountingJournalSequenceMixin(BehaviorForm):
    accounting_journal_sequence = forms.CharField(
        label=_(
            "type accounting journal sequence to confirm migration",
        ).upper(),
        max_length=255,
        required=True,
        widget=get_input_datalist_widget(
            model=models.Voucher,
            field_name="accounting_journal_sequence",
            placeholder=_("e.g. JOV000001 2025"),
        ),
    )


class VoucherBulkMigrateForm(AccountingJournalSequenceMixin):
    action_check = forms.ModelMultipleChoiceField(
        queryset=models.Voucher.objects.all(),
    )

    def save(self):
        queryset: QuerySet = self.cleaned_data.get("action_check")
        accounting_journal_sequence = self.cleaned_data.get(
            "accounting_journal_sequence"
        )

        queryset.update(accounting_journal_sequence=accounting_journal_sequence)


class VoucherMigrateForm(AccountingJournalSequenceMixin):
    slug = forms.CharField(required=True)

    def save(self):
        slug = self.cleaned_data["slug"]
        accounting_journal_sequence = self.cleaned_data.get(
            "accounting_journal_sequence"
        )

        voucher = get_object_or_404(models.Voucher, slug=slug)
        voucher.accounting_journal_sequence = accounting_journal_sequence
        voucher.save(audit=True)


class BaseVoucherForm(CustomModelForm):
    period = get_autocomplete_field(
        Period.objects.all(),
        to_field_name="name",
        widget_attributes={"placeholder": _("search periods")},
        field_attributes={"label": _("period")},
        app_label="fin",
        model_name="Period",
        object_name="period",
        field_name="search",
    )
    kind = get_autocomplete_field(
        VoucherKind.objects.all(),
        to_field_name="name",
        widget_attributes={"placeholder": _("search voucher kinds")},
        field_attributes={"label": _("kind")},
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
            "document": get_file_widget(placeholder=_("voucher document")),
        }


class VoucherForm(BaseVoucherForm):
    pass
