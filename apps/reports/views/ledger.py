from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import View

from apps.core import mixins
from apps.hr.models import Employee
from apps.trans.filters import LedgerFilter
from apps.trans.models import JournalEntry

# from ..resources import LedgerResource


class LedgerView(
    mixins.PaginationMixin,
    mixins.TemplateVariablesMixin,
    mixins.SearchFilterMixin,
    mixins.TemplateNamesMixin,
    mixins.SidebarFilterMixin,
    View,
):
    model = JournalEntry
    app_label = "reports"
    verbose_name_plural = "ledger"
    filter_class = LedgerFilter

    def get(self, request: HttpRequest, slug: str, *args, **kwargs):
        self.employee = get_object_or_404(Employee, slug=slug)

        queryset = JournalEntry.objects.filter(employee=self.employee)

        filter_obj = LedgerFilter(request.GET, queryset)
        queryset = filter_obj.qs

        SearchFilter = self.get_search_filter_class()
        search_filter = SearchFilter(request.GET, queryset=queryset)
        queryset = search_filter.qs

        if request.GET.get("filters"):
            template_name = self.get_filter_form_template_name()
            context = self.sidebar_filters_context_data(request, queryset)
            return self.get_filters_response(request, template_name, context)

        page = self.get_page_class(request, queryset)

        if request.htmx:
            template_name = self.get_table_template_name()
        else:
            template_name = self.get_template_name()

        context = {
            "employee": self.employee,
            "page": page,
            "search_filter": search_filter,
            "app_label": "reports",
            "subapp_label": "ledger",
            "model_name": JournalEntry._meta.model_name,
            "model": JournalEntry,
            **self.get_create_url(),
            **self.get_index_url(),
            **self.get_html_ids(),
            **self.get_permissions(request),
        }

        return render(request, template_name, context)

    def get_index_url(self):
        return {
            "index_url": reverse(
                f"{self.app_label}:{self.verbose_name_plural}",
                kwargs={"slug": self.employee.slug},
            )
        }
