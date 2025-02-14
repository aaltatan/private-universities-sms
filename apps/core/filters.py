from typing import Any, Mapping

import django_filters as filters
from django.db.models import Model, Q, QuerySet

from .utils import get_djangoql_query, get_keywords_query
from .widgets import ComboboxWidget, OrderingWidget


class FilterTextMixin:
    """
    A mixin that adds a text filter to a model.
    """

    def filter_text(self, qs, name, value):
        if not value:
            return qs

        query = get_keywords_query(value)
        return qs.filter(query)


class FilterComboboxMixin:
    """
    A mixin that add a filter_combobox to a model.
    """

    def filter_combobox(self, qs, name, value):
        if not value:
            return qs

        stmt = Q(**{f"{name}__in": value})

        return qs.filter(stmt).distinct()


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


def get_combobox_choices_filter(
    model: Model,
    field_name: str,
    label: str,
    method_name: str = "filter_combobox",
    choices: Any = None,
    api_filter: bool = False,
) -> filters.MultipleChoiceFilter:
    """
    you must define a filter_combobox method in the model or useFilterComboboxMixin .
    """
    kwargs = {
        "field_name": field_name,
        "label": label,
        "method": method_name,
    }

    if not api_filter:
        kwargs["widget"] = ComboboxWidget(
            attrs={"data-name": label},
        )

    if choices is not None:
        kwargs["choices"] = choices
    else:
        values_list = model.objects.values_list(field_name, flat=True)
        values_list = sorted([(f, f) for f in set(values_list)])
        kwargs["choices"] = values_list

    return filters.MultipleChoiceFilter(**kwargs)
