from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import View

from apps.core import mixins
from apps.org.models import CostCenter

from .. import filters, resources


class CostCenterView(PermissionRequiredMixin, mixins.ListMixin, View):
    app_label = "reports"
    codename_plural = "cost_centers"
    permission_required = "reports.view_costcenter"
    model = CostCenter
    filter_class = filters.CostCenterFilter
    resource_class = resources.CostCenterResource
    ordering_fields = {
        "name": _("name"),
        "total_debit": _("total debit"),
        "total_credit": _("total credit"),
        "total_amount": _("total amount"),
    }

    def get_queryset(self):
        return (
            CostCenter.objects.annotate_journals_total_debit()
            .annotate_journals_total_credit()
            .annotate_journals_total_amount()
            .order_by("-total_amount", "name")
        )

    def get_index_url(self):
        return reverse("reports:cost_center:index")

    def get_dataset_title(self):
        return "Cost Center"
