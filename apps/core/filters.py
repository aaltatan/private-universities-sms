from typing import Any, Callable, Literal, Mapping

import django_filters as filters
from django import forms
from django.db.models import Q, QuerySet
from django.forms import TextInput
from django.utils.translation import gettext as _

from .utils import get_djangoql_query, get_keywords_query
from .widgets import (
    ComboboxWidget,
    OrderingWidget,
    get_date_widget,
    get_email_widget,
    get_text_widget,
    get_url_widget,
)


class FilterTextMixin:
    """
    A mixin that adds a text filter to a model.
    """

    def filter_text(self, qs, name, value):
        if not value:
            return qs

        is_reversed = value.startswith("!")

        if is_reversed:
            value = value[1:]

        query = get_keywords_query(
            value,
            field_name=name,
            is_reversed=is_reversed,
        )
        return qs.filter(query)


class FilterComboboxMixin:
    """
    A mixin that add a filter_combobox to a model.
    """

    def filter_combobox_combined(self, qs, name, value):
        if not value:
            return qs

        for obj in value:
            qs = qs.filter(**{name: obj})

        return qs

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


class CustomOrderingFilter(filters.OrderingFilter):
    descending_fmt = _("%s (desc)")


def get_ordering_filter(fields: Mapping[str, str]) -> CustomOrderingFilter:
    """
    Returns an OrderingFilter.
    """
    return CustomOrderingFilter(
        fields=list(fields.keys()),
        field_labels=fields,
        widget=OrderingWidget,
    )


def get_combobox_choices_filter(
    queryset: QuerySet,
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
        return filters.MultipleChoiceFilter(**kwargs)
    else:
        if type(queryset) == QuerySet:
            kwargs["choices"] = (
                queryset.values_list(field_name, field_name)
                .order_by(field_name)
                .distinct()
            )
            return filters.MultipleChoiceFilter(**kwargs)
        else:  # if is a function
            kwargs["queryset"] = queryset
            return filters.ModelMultipleChoiceFilter(**kwargs)


def get_text_filter(
    label: str,
    exact: bool = False,
    field_name: str | None = None,
    method_name: str = "filter_text",
    widget_type: Literal["text", "email", "url"] = "text",
    **widget_attributes: dict[str, str],
) -> filters.CharFilter:
    if "placeholder" not in widget_attributes:
        widget_attributes.setdefault("placeholder", label)

    widgets: dict[str, Callable[..., TextInput]] = {
        "text": get_text_widget,
        "email": get_email_widget,
        "url": get_url_widget,
    }

    kwargs = {
        "label": label,
        "widget": widgets.get(widget_type, get_text_widget)(
            **widget_attributes,
        ),
    }

    if exact:
        kwargs["lookup_expr"] = "exact"
    else:
        kwargs["method"] = method_name

    if field_name is not None:
        kwargs["field_name"] = field_name

    return filters.CharFilter(**kwargs)


def get_number_from_to_filters(
    field_name: str,
    method_name: str | None = None,
    from_attributes: dict[str, str] = {},
    to_attributes: dict[str, str] = {},
) -> tuple[filters.NumberFilter, filters.NumberFilter]:
    """
    Get number range fields.

    Args:
        field_name (str): The name of the field.
        method_name (str | None, optional): The name of the method to call. Defaults to None you must name the method filter_{field_name}_from and filter_{field_name}_to.
        from_attributes (dict[str, str], optional): The attributes for the from field. Defaults to {}.
        to_attributes (dict[str, str], optional): The attributes for the to field. Defaults to {}.
    """

    from_attributes.setdefault("placeholder", _("from").title())
    to_attributes.setdefault("placeholder", _("to").title())

    from_kwargs = {
        "field_name": field_name,
        "widget": get_text_widget(**from_attributes),
    }

    to_kwargs = {
        "field_name": field_name,
        "widget": get_text_widget(**to_attributes),
    }

    if method_name is not None:
        from_kwargs["method"] = f"{method_name}_from"
        to_kwargs["method"] = f"{method_name}_to"
    else:
        from_kwargs["lookup_expr"] = "gte"
        to_kwargs["lookup_expr"] = "lte"

    from_ = filters.NumberFilter(**from_kwargs)
    to = filters.NumberFilter(**to_kwargs)

    return from_, to


def get_date_from_to_filters(
    field_name: str,
    from_attributes: dict[str, str] = {},
    to_attributes: dict[str, str] = {},
) -> tuple[filters.DateFilter, filters.DateFilter]:
    """Get number range fields."""

    from_attributes.setdefault("placeholder", _("from").title())
    from_attributes.setdefault("x-mask", "9999-99-99")
    to_attributes.setdefault("placeholder", _("to").title())
    to_attributes.setdefault("x-mask", "9999-99-99")

    from_ = filters.DateFilter(
        field_name=field_name,
        lookup_expr="gte",
        widget=get_date_widget(**from_attributes, fill_onfocus=False),
    )
    to = filters.DateFilter(
        field_name=field_name,
        lookup_expr="lte",
        widget=get_date_widget(**to_attributes, fill_onfocus=False),
    )

    return from_, to


class BaseNameDescriptionFilter(FilterTextMixin, filters.FilterSet):
    """
    a base class for filters that have **(name)** and **(description)** fields.
    """

    name = get_text_filter(label=_("name").title())
    description = get_text_filter(label=_("description").title())


class BaseQSearchFilter(FilterSearchMixin, filters.FilterSet):
    """
    a base class for filters that have a search field **(q)**.
    """

    q = filters.CharFilter(
        method="search",
        widget=forms.TextInput(
            attrs={
                "placeholder": _("search").title(),
            },
        ),
    )
