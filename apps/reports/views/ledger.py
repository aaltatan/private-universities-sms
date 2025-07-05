from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import resolve, reverse
from django.views.generic import View
from django.views.generic.list import MultipleObjectMixin

from apps.core import mixins
from apps.hr.models import Employee
from apps.trans.filters import LedgerFilter
from apps.trans.models import JournalEntry

from .. import resources


class LedgerView(
    PermissionRequiredMixin,
    mixins.ListMixin,
    MultipleObjectMixin,
    View,
):
    app_label = "reports"
    verbose_name_plural = "ledger"
    permission_required = "trans.view_journalentry"
    model = JournalEntry
    filter_class = LedgerFilter
    resource_class = resources.LedgerResource
    order_filter = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employee"] = self.employee
        return context

    def get_initial_queryset(self):
        resolved = resolve(self.request.path_info)
        slug = resolved.kwargs.get("slug")

        self.employee = get_object_or_404(Employee, slug=slug)

        return JournalEntry.objects.filter(employee=self.employee)

    def get_index_url(self):
        return reverse("reports:ledger", kwargs={"slug": self.employee.slug})

    def get_dataset_title(self):
        return self.employee.fullname
