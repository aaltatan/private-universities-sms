from urllib.parse import urlencode

from django.db.models import QuerySet
from django.forms.widgets import SelectMultiple, TextInput
from django.template.loader import render_to_string

from .fields import CustomModelChoiceField


class RenderMixin:
    """Render mixin."""

    def render(self, name, value, attrs=..., renderer=...):
        context = self.get_context(name, value, attrs)
        return render_to_string(self.template_name, context)


class AutocompleteWidget(RenderMixin, TextInput):
    """
    An extended TextInput widget that renders an autocomplete.
    """

    template_name = "widgets/autocomplete.html"


class ComboboxWidget(RenderMixin, SelectMultiple):
    """
    An extended SelectMultiple widget that renders a combobox.
    """

    template_name = "widgets/combobox.html"
    checked_attribute = {"checked": True}


class OrderByWidget(RenderMixin, SelectMultiple):
    """
    An extended SelectMultiple widget that order functionality and styling.
    """

    template_name = "widgets/order_by.html"


def get_autocomplete_field(
    queryset: QuerySet,
    to_field_name: str = "pk",
    **kwargs: dict[str, str],
) -> CustomModelChoiceField:
    """Get autocomplete field."""

    kwargs.setdefault("label_field_name", to_field_name)

    return CustomModelChoiceField(
        queryset=queryset,
        to_field_name=to_field_name,
        widget=AutocompleteWidget({"querystring": urlencode(kwargs)}),
    )
