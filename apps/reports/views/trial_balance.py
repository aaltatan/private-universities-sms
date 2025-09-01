from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import View

from apps.core import mixins
from apps.hr.models import Employee

from .. import filters, resources


class TrialBalanceView(PermissionRequiredMixin, mixins.ListMixin, View):
    app_label = "reports"
    codename_plural = "trial_balance"
    permission_required = "reports.view_trialbalance"
    model = Employee
    filter_class = filters.TrialBalanceFilter
    resource_class = resources.TrialBalanceResource
    ordering_fields = {
        "fullname": _("fullname"),
        "total_debit": _("total debit"),
        "total_credit": _("total credit"),
        "total_amount": _("total amount"),
    }

    def get_queryset(self):
        return (
            Employee.objects.annotate_journals_total_debit(filter_compensations=False)
            .annotate_journals_total_credit(filter_compensations=False)
            .annotate_journals_total_amount(filter_compensations=False)
            .order_by("-total_amount", "fullname")
        )

    def get_index_url(self):
        return reverse("reports:trial_balance:index")

    def get_dataset_title(self):
        return "Trial Balance"
