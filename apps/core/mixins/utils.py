from abc import ABC, abstractmethod

import django_filters as filters
from djangoql.admin import DjangoQLSearchMixin, apply_search


class CustomDjangoQLSearchMixin(DjangoQLSearchMixin):
    def get_search_results(self, request, queryset, search_term):
        if not search_term:
            return queryset, False
        qs = apply_search(queryset, search_term, self.djangoql_schema)
        return qs, False


class FiltersetMixin(ABC):
    @property
    @abstractmethod
    def filterset_class(self) -> type[filters.FilterSet]:
        pass

    def get_queryset(self):
        qs = super().get_queryset()
        filterset = self.filterset_class(self.request.GET, queryset=qs)
        return filterset.qs

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs["filter"] = self.filterset_class(self.request.GET)
        return kwargs
