from typing import Mapping

import django_filters as filters
from django.db.models import QuerySet

from .utils import get_djangoql_query, get_keywords_query
from .widgets import OrderingWidget


class FilterSearchMixin:
    """
    A mixin that adds a search filter to a model.
    """

    def search(
        self,
        queryset: QuerySet,
        name: str,
        value: str,
    ) -> QuerySet:
        """
        Searches the queryset for the given name and value.
        """
        default_queryset = queryset.filter(get_keywords_query(value))
        return get_djangoql_query(queryset, value, default_queryset)


def get_ordering_filter(fields: Mapping[str, str]) -> filters.OrderingFilter:
    """
    Returns an OrderingFilter.
    """
    return filters.OrderingFilter(
        fields=list(fields.items()),
        widget=OrderingWidget,
    )
