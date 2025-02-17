from typing import Any, Mapping

import django_filters as filters
from django.db.models import Model, Q, QuerySet
from django.utils.translation import gettext as _

from .utils import get_djangoql_query, get_keywords_query
from .widgets import ComboboxWidget, OrderingWidget, get_text_widget


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
        kwargs["choices"] = (
            model.objects.values_list(field_name, field_name)
            .order_by(field_name)
            .distinct()
        )

    return filters.MultipleChoiceFilter(**kwargs)


def get_text_filter(
    label: str,
    method_name: str = "filter_text",
    **widget_attributes: dict[str, str],
) -> filters.CharFilter:
    if "placeholder" not in widget_attributes:
        widget_attributes.setdefault("placeholder", label)

    return filters.CharFilter(
        label=label,
        method=method_name,
        widget=get_text_widget(**widget_attributes),
    )


def get_number_from_to_filters(
    field_name: str,
    from_attributes: dict[str, str] = {},
    to_attributes: dict[str, str] = {},
) -> tuple[filters.NumberFilter, filters.NumberFilter]:
    """Get number range fields."""

    from_attributes.setdefault("placeholder", _("from").title())
    from_attributes.setdefault("x-mask", "9999999999")
    to_attributes.setdefault("placeholder", _("to").title())
    to_attributes.setdefault("x-mask", "9999999999")

    from_ = filters.NumberFilter(
        field_name=field_name,
        lookup_expr="gte",
        widget=get_text_widget(**from_attributes),
    )
    to = filters.NumberFilter(
        field_name=field_name,
        lookup_expr="lte",
        widget=get_text_widget(**to_attributes),
    )

    return from_, to
