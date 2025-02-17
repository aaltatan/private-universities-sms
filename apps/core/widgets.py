from django.forms.widgets import SelectMultiple, Textarea, TextInput
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


class OrderingWidget(RenderMixin, SelectMultiple):
    """
    An extended SelectMultiple widget that order functionality and styling.
    """

    template_name = "widgets/ordering.html"


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


def get_text_widget(**attributes: dict[str, str]) -> TextInput:
    """Get text field."""
    return TextInput(attrs=attributes)
