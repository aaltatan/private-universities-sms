from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import View

from apps.core import mixins
from apps.fin.models import Period

from .. import filters, resources


class PeriodsView(PermissionRequiredMixin, mixins.ListMixin, View):
    app_label = "reports"
    codename_plural = "periods"
    permission_required = "reports.view_period"
    model = Period
    filter_class = filters.PeriodFilter
    resource_class = resources.PeriodResource
    ordering_fields = {
        "name": _("name"),
        "total_debit": _("total debit"),
        "total_credit": _("total credit"),
        "total_amount": _("total amount"),
    }

    def get_queryset(self):
        return (
            Period.objects.annotate_journals_total_debit()
            .annotate_journals_total_credit()
            .annotate_journals_total_amount()
            .order_by("name")
        )

    def get_index_url(self):
        return reverse("reports:periods:index")

    def get_dataset_title(self):
        return "Period"
