from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils import timezone
from django.views.generic import ListView

from apps.core.mixins import FiltersetMixin

from .. import filters, models


class UpcomingBirthdaysView(PermissionRequiredMixin, FiltersetMixin, ListView):
    permission_required = "hr.view_employee"
    template_name = "components/hr/employees/widgets/upcoming-birthdays.html"
    queryset = models.Employee.objects.all()
    filterset_class = filters.UpcomingBirthdaysFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.datetime.now()
        return context


class UpcomingJobAnniversariesView(PermissionRequiredMixin, FiltersetMixin, ListView):
    permission_required = "hr.view_employee"
    template_name = "components/hr/employees/widgets/upcoming-job-anniversaries.html"
    queryset = models.Employee.objects.all()
    filterset_class = filters.UpcomingJobAnniversariesFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.datetime.now()
        return context


class GroupByCountsView(PermissionRequiredMixin, FiltersetMixin, ListView):
    permission_required = "hr.view_employee"
    template_name = "components/hr/employees/widgets/group-by-counts.html"
    queryset = models.Employee.objects.all()
    filterset_class = filters.GroupedByCountsFilter
