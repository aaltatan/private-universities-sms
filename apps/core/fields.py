import json
from typing import Any
from urllib.parse import urlencode

from django.db.models import QuerySet
from django.forms import FileInput, ModelChoiceField
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .widgets import AutocompleteWidget


class CustomModelChoiceField(ModelChoiceField):
    """A custom ModelChoiceField."""

    default_error_messages = {
        "invalid_choice": _("this choice is not valid"),
    }


def get_avatar_field(url: str, **kwargs: dict[str, str]) -> FileInput:
    attrs = {
        "hx-get": reverse_lazy(url, kwargs=kwargs),
        "hx-trigger": "load",
        "hx-target": "this",
    }

    return FileInput(attrs)


def get_autocomplete_field(
    queryset: QuerySet,
    to_field_name: str = "pk",
    widget_attributes: dict[str, str] = {},
    field_attributes: dict[str, Any] = {},
    queryset_filters: dict[str, Any] = {},
    **kwargs: dict[str, str],
) -> CustomModelChoiceField:
    """Get autocomplete field."""

    if "placeholder" not in widget_attributes:
        widget_attributes["placeholder"] = _("search").title()
    else:
        widget_attributes["placeholder"] = widget_attributes["placeholder"].title()

    kwargs.setdefault("label_field_name", to_field_name)

    return CustomModelChoiceField(
        queryset=queryset,
        to_field_name=to_field_name,
        widget=AutocompleteWidget(
            {
                "querystring": urlencode(kwargs),
                "queryset_filters": json.dumps(queryset_filters),
                **widget_attributes,
            }
        ),
        **field_attributes,
    )
