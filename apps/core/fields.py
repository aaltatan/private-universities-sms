from urllib.parse import urlencode

from django.db.models import QuerySet
from django.forms import ModelChoiceField
from django.utils.translation import gettext_lazy as _

from .widgets import AutocompleteWidget


class CustomModelChoiceField(ModelChoiceField):
    """A custom ModelChoiceField."""

    default_error_messages = {
        "invalid_choice": _("this choice is not valid"),
    }


def get_autocomplete_field(
    queryset: QuerySet,
    to_field_name: str = "pk",
    attributes: dict[str, str] = {},
    **kwargs: dict[str, str],
) -> CustomModelChoiceField:
    """Get autocomplete field."""

    if "placeholder" not in attributes:
        attributes["placeholder"] = _("search").title()
    else:
        attributes["placeholder"] = attributes["placeholder"].title()

    kwargs.setdefault("label_field_name", to_field_name)

    return CustomModelChoiceField(
        queryset=queryset,
        to_field_name=to_field_name,
        widget=AutocompleteWidget(
            {
                "querystring": urlencode(kwargs),
                **attributes,
            }
        ),
    )
