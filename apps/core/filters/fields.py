from typing import Any, Literal, Mapping, Callable

import django_filters as filters
from django.db.models import Model
from django.forms import TextInput
from django.utils.translation import gettext as _

from ..widgets import (
    ComboboxWidget,
    OrderingWidget,
    get_email_widget,
    get_text_widget,
    get_url_widget,
    get_date_widget,
)


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
    exact: bool = False,
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

    return filters.CharFilter(**kwargs)


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
