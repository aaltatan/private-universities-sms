from typing import Literal, Sequence

from django.db.models import Q, QuerySet
from djangoql.exceptions import (
    DjangoQLError,
    DjangoQLLexerError,
    DjangoQLParserError,
)
from djangoql.queryset import apply_search


def get_keywords_query(
    value: str,
    field_name: str = "search",
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
        kwargs = {f"{field_name}__icontains": word}
        if join == "and":
            query &= Q(**kwargs)
        else:
            query |= Q(**kwargs)

    return query


def get_djangoql_query(
    qs_to_filter: QuerySet,
    djangoql_query: str,
    default_queryset: QuerySet,
) -> QuerySet:
    """
    Returns a queryset filtered by a DjangoQL query.
    """
    try:
        queryset = apply_search(qs_to_filter, djangoql_query)
    except (
        DjangoQLError,
        DjangoQLParserError,
        DjangoQLLexerError,
    ):
        queryset = default_queryset

    return queryset
