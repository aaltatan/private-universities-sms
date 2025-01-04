from typing import Literal, Mapping, Sequence

import django_filters as filters
from django.db.models import QuerySet, Q
from djangoql.exceptions import (
    DjangoQLError,
    DjangoQLLexerError,
    DjangoQLParserError,
)
from djangoql.queryset import apply_search

from .widgets import OrderByWidget


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
        try:
            queryset = apply_search(queryset, value)
        except (
            DjangoQLError,
            DjangoQLParserError,
            DjangoQLLexerError,
        ):
            query = self.__search(value)
            queryset = queryset.filter(query)

        return queryset

    def __search(
        self,
        value: str,
        join: Literal["and", "or"] = "and",
        type: Literal["word", "letter"] = "word",
    ) -> Q:
        """
        Returns a search query.
        """
        query: Q = Q()
        keywords: Sequence[str] = ""

        if type == "word":
            keywords = value.split(" ")
        elif type == "letter":
            keywords = value

        for word in keywords:
            if join == "and":
                query &= Q(search__icontains=word)
            else:
                query |= Q(search__icontains=word)

        return query


def get_order_by_filter(fields: Mapping[str, str]) -> filters.OrderingFilter:
    """
    Returns an OrderingFilter.
    """
    return filters.OrderingFilter(
        fields=list(fields.items()),
        widget=OrderByWidget,
    )
