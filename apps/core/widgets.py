from typing import Iterable

from django.db import models
from django.forms.widgets import (
    DateInput,
    FileInput,
    Input,
    SelectMultiple,
    Textarea,
    TextInput,
    NumberInput,
)
from django.template.loader import render_to_string
from django.utils.translation import gettext as _


class RenderMixin:
    """Render mixin."""

    def render(self, name, value, attrs=..., renderer=...):
        context = self.get_context(name, value, attrs)
        return render_to_string(self.template_name, context)


class DateWidget(DateInput):
    template_name = "widgets/date.html"

    def __init__(self, attrs=None, format=None, fill_onfocus: bool = True):
        self.fill_onfocus = fill_onfocus
        super().__init__(attrs, format)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["fill_onfocus"] = self.fill_onfocus
        return context


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


class SelectMultipleWidget(RenderMixin, SelectMultiple):
    """
    An extended SelectMultiple widget that renders a select multiple.
    """

    template_name = "widgets/select-multiple.html"
    checked_attribute = {"checked": True}


class TextWithDataListInputWidget(Input):
    input_type = "text"
    template_name = "widgets/text-datalist.html"

    def __init__(self, attrs=None, datalist: Iterable | None = None) -> None:
        self.datalist = datalist
        super().__init__(attrs)

    def get_context(self, *args, **kwargs) -> dict:
        context = super().get_context(*args, **kwargs)
        context["datalist"] = self.datalist
        return context


class AvatarWidget(RenderMixin, FileInput):
    """
    An extended FileInput widget that renders an avatar.
    """

    template_name = "widgets/avatar.html"


class OrderingWidget(RenderMixin, SelectMultiple):
    """
    An extended SelectMultiple widget that order functionality and styling.
    """

    template_name = "widgets/ordering.html"


def get_textarea_widget(
    rows: int = 1,
    **attributes: dict[str, str],
) -> Textarea:
    """Get textarea field with x-autosize attribute."""

    if "placeholder" not in attributes:
        attributes.setdefault(
            "placeholder",
            _("some description").title(),
        )
    else:
        attributes["placeholder"] = attributes["placeholder"].title()

    return Textarea(
        attrs={"rows": rows, "x-autosize": "", **attributes},
    )


def get_numeric_widget(
    x_mask: str = "9999999999",
    **attributes: dict[str, str],
) -> TextInput:
    """Get numeric field with x-mask attribute."""
    if "placeholder" in attributes:
        attributes["placeholder"] = attributes["placeholder"].title()
    return TextInput(
        attrs={
            "x-mask": x_mask,
            **attributes,
        },
    )


def get_money_widget(
    decimal_separator: str = ".",
    thousands_separator: str = ",",
    decimal_places: int = 4,
    **attributes: dict[str, str],
) -> TextInput:
    """Get numeric field with x-mask attribute."""
    if "placeholder" in attributes:
        attributes["placeholder"] = attributes["placeholder"].title()
    else:
        attributes["placeholder"] = "0." + "0" * decimal_places

    return TextInput(
        attrs={
            "x-mask:dynamic": f"$money($input, '{decimal_separator}', '{thousands_separator}', {decimal_places})",
            **attributes,
        },
    )


def get_text_widget(**attributes: dict[str, str]) -> TextInput:
    """Get text field."""
    return TextInput(attrs=attributes)


def get_number_widget(**attributes: dict[str, str]) -> TextInput:
    """Get text field."""
    return NumberInput(attrs=attributes)


def get_email_widget(**attributes: dict[str, str]) -> TextInput:
    """Get email field."""
    if "placeholder" not in attributes:
        attributes.setdefault("placeholder", _("some-email@example.com"))
    return TextInput(
        attrs={
            "type": "email",
            **attributes,
        },
    )


def get_url_widget(**attributes: dict[str, str]) -> TextInput:
    """Get url field."""
    if "placeholder" not in attributes:
        attributes.setdefault("placeholder", "https://example.com")
    return TextInput(attrs=attributes)


def get_date_widget(
    fill_onfocus: bool = True,
    **attributes: dict[str, str],
) -> DateWidget:
    """Get date field."""
    return DateWidget(fill_onfocus=fill_onfocus, attrs=attributes)


def get_input_datalist(
    model: models.Model, field_name: str, **attrs
) -> TextWithDataListInputWidget:
    return TextWithDataListInputWidget(
        attrs=attrs,
        datalist=model.objects.values_list(field_name, flat=True)
        .order_by(field_name)
        .distinct(),
    )
