import json

from django import forms
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


def get_autocomplete_field(**kwargs: dict[str, str]) -> forms.CharField:
    """Get autocomplete field."""
    return forms.CharField(
        widget=AutocompleteWidget({"data-data": json.dumps(kwargs)}),
    )
