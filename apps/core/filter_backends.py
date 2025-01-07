from django.http import HttpRequest
from django.db.models import QuerySet

from rest_framework import filters
from djangoql.exceptions import (
    DjangoQLError,
    DjangoQLParserError,
    DjangoQLLexerError,
)
from djangoql.queryset import apply_search


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

        try:
            queryset = apply_search(queryset, value)
        except (
            DjangoQLError,
            DjangoQLParserError,
            DjangoQLLexerError,
        ):
            queryset = super().filter_queryset(request, queryset, view)

        return queryset
