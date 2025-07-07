from typing import Callable

from django.db.models import Model, QuerySet
from django.http import HttpRequest
from django.urls import resolve
from django.utils.translation import gettext_lazy as _

from apps.core.filters import get_combobox_choices_filter
from apps.org.models import CostCenter
from apps.trans.models import Voucher

from apps.trans.filters import BaseJournalEntryLedgerFilter


def get_ledger_filtered_queryset(
    model: type[Model],
) -> Callable[[HttpRequest], QuerySet]:
    def inner(request: HttpRequest) -> QuerySet:
        resolved = resolve(request.path_info)
        slug = resolved.kwargs.get("slug")
        return model.objects.filter(journals__employee__slug=slug)

    return inner


class LedgerFilter(BaseJournalEntryLedgerFilter):
    cost_center = get_combobox_choices_filter(
        queryset=get_ledger_filtered_queryset(CostCenter),
        field_name="cost_center",
        label=_("cost center"),
    )
    voucher = get_combobox_choices_filter(
        queryset=get_ledger_filtered_queryset(model=Voucher),
        field_name="voucher",
        label=_("voucher".title()),
    )
