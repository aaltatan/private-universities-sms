import json

from django import forms
from django.db.models import QuerySet
from django.forms.widgets import SelectMultiple, TextInput
from django.template.loader import render_to_string


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
    **kwargs: dict[str, str],
) -> forms.ModelChoiceField:
    """Get autocomplete field."""
    return forms.ModelChoiceField(
        queryset=queryset,
        widget=AutocompleteWidget({"data-data": json.dumps(kwargs)}),
    )
