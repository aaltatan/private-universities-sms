from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import View

from apps.core import mixins
from apps.fin.models import Compensation

from .. import filters, resources


class CompensationsView(PermissionRequiredMixin, mixins.ListMixin, View):
    app_label = "reports"
    codename_plural = "compensations"
    permission_required = "reports.view_compensation"
    model = Compensation
    filter_class = filters.CompensationFilter
    resource_class = resources.CompensationResource
    ordering_fields = {
        "name": _("name"),
        "total_debit": _("total debit"),
        "total_credit": _("total credit"),
        "total_amount": _("total amount"),
    }

    def get_queryset(self):
        return (
            Compensation.objects.annotate_journals_total_debit()
            .annotate_journals_total_credit()
            .annotate_journals_total_amount()
            .order_by("name")
        )

    def get_index_url(self):
        return reverse("reports:compensations:index")

    def get_dataset_title(self):
        return "Compensation"
