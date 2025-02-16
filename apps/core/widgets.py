from urllib.parse import urlencode

from django.db.models import QuerySet
from django.forms import ModelChoiceField
from django.forms.widgets import SelectMultiple, Textarea, TextInput
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _


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


class OrderingWidget(RenderMixin, SelectMultiple):
    """
    An extended SelectMultiple widget that order functionality and styling.
    """

    template_name = "widgets/ordering.html"


class CustomModelChoiceField(ModelChoiceField):
    """A custom ModelChoiceField."""

    default_error_messages = {
        "invalid_choice": _("this choice is not valid"),
    }


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


def get_textarea_widget(rows: int = 1) -> Textarea:
    """Get textarea field with x-autosize attribute."""
    return Textarea(
        attrs={
            "rows": rows,
            "x-autosize": "",
        },
    )


def get_numeric_widget(x_mask: str = "9999999999") -> TextInput:
    """Get numeric field with x-mask attribute."""
    return TextInput(
        attrs={
            "x-mask": x_mask,
        },
    )
