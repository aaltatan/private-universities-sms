from django.db.models import QuerySet
from django.http import HttpRequest
from rest_framework import filters

from .utils import get_djangoql_query


class DjangoQLSearchFilter(filters.SearchFilter):
    """
    a SearchFilter that uses DjangoQL to search the queryset.
    """

    def filter_queryset(
        self,
        request: HttpRequest,
        queryset: QuerySet,
        view,
    ):
        value = request.GET.get(self.search_param)

        if not value:
            return super().filter_queryset(request, queryset, view)

        default_queryset = super().filter_queryset(request, queryset, view)

        return get_djangoql_query(queryset, value, default_queryset)
