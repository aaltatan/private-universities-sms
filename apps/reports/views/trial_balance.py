from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
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
    order_filter = False

    def get_index_url(self):
        return reverse("reports:trial_balance:index")

    def get_dataset_title(self):
        return "Trial Balance"
