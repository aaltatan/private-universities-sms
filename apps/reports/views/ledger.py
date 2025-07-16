from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import resolve, reverse
from django.views.generic import View
from django.db import models

from apps.core import mixins
from apps.core.models import Template
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


class ExportToMSWordView(
    PermissionRequiredMixin,
    mixins.ExportToMSWordMixin,
    View,
):
    permission_required = "reports.export_ledger"

    def get_template(self):
        return Template.get_ledger_template()

    def get_filename(self):
        return self.employee.national_id

    def get_context_data(self):
        resolved = resolve(self.request.path_info)
        self.employee = get_object_or_404(Employee, slug=resolved.kwargs.get("slug"))

        queryset = JournalEntry.objects.filter(employee=self.employee)

        filter_obj = filters.LedgerFilter(
            self.request.GET, queryset, request=self.request
        )

        totals = filter_obj.qs.aggregate(
            total_debit=models.Sum("debit"),
            total_credit=models.Sum("credit"),
        )

        total_debit = totals["total_debit"] or 0
        total_credit = totals["total_credit"] or 0
        net = total_debit - total_credit

        total_debit = f"{total_debit:,.2f}"
        total_credit = f"{total_credit:,.2f}"
        net = f"{net:,.2f}"

        return {
            "employee": self.employee,
            "qs": filter_obj.qs,
            "total_debit": total_debit,
            "total_credit": total_credit,
            "net": net,
        }
