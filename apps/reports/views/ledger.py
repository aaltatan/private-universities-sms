from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import resolve, reverse
from django.views.generic import View

from apps.core import mixins
from apps.hr.models import Employee
from apps.trans.models import JournalEntry

from .. import resources, filters


class LedgerView(PermissionRequiredMixin, mixins.ListMixin, View):
    app_label = "reports"
    codename_plural = "ledger"
    permission_required = "reports.view_ledger"
    model = JournalEntry
    filter_class = filters.LedgerFilter
    resource_class = resources.LedgerResource
    order_filter = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employee"] = self.employee
        return context

    def get_queryset(self):
        resolved = resolve(self.request.path_info)
        slug = resolved.kwargs.get("slug")

        self.employee = get_object_or_404(Employee, slug=slug)

        return JournalEntry.objects.filter(employee=self.employee)

    def get_index_url(self):
        return reverse("reports:ledger:index", kwargs={"slug": self.employee.slug})

    def get_dataset_title(self):
        return self.employee.fullname
