from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import View

from apps.core import mixins
from apps.hr.models import Employee

from .. import filters, resources


class EmployeesView(PermissionRequiredMixin, mixins.ListMixin, View):
    app_label = "reports"
    codename_plural = "employees"
    permission_required = "reports.view_employee"
    model = Employee
    filter_class = filters.EmployeeFilter
    resource_class = resources.EmployeeResource
    ordering_fields = {
        "name": _("name"),
        "total_debit": _("total debit"),
        "total_credit": _("total credit"),
        "total_amount": _("total amount"),
    }

    def get_queryset(self):
        return (
            Employee.objects.annotate_journals_total_debit()
            .annotate_journals_total_credit()
            .annotate_journals_total_amount()
            .order_by("-total_amount", "fullname")
        )

    def get_index_url(self):
        return reverse("reports:employees:index")

    def get_dataset_title(self):
        return "Employee"
