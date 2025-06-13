from decimal import Decimal
from typing import Literal

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


def _format_string(
    value: str,
    chars_width: int = 15,
    in_table: bool = False,
    color: Literal["red", "green", "none"] = "none",
) -> str:
    right_result = value.rjust(chars_width)
    left_result = value.ljust(chars_width)

    text_color = "" if color == "none" else f"style='color: {color}'"

    if in_table:
        return mark_safe(
            f"""
            <pre {text_color} class='rtl:hidden @max-lg:hidden font-medium'>{right_result}</pre>
            <pre {text_color} class='ltr:hidden @max-lg:hidden font-medium'>{left_result}</pre>
            <pre {text_color} class='@lg:hidden font-medium'>{value}</pre>
            """,
        )
    else:
        return mark_safe(f"<pre {text_color} class='font-medium'>{value}</pre>")


@register.filter
def percentage(
    value: float | Decimal | int,
    in_table: bool = False,
    decimal_places: int = 2,
) -> str:
    result = f"{value * 100:.{decimal_places}f} %"
    return _format_string(result, in_table=in_table, chars_width=10)


@register.filter
def money(
    value: float | Decimal | int | str,
    in_table: bool = False,
    decimal_places: int = 2,
    chars_width: int = 15,
) -> str:
    if value == "":
        return "0"

    if not isinstance(value, str):
        if value < 0:
            value = abs(value)
            result = f"({value:,.{decimal_places}f})"
        else:
            result = f"{value:,.{decimal_places}f}"

    return _format_string(
        result,
        in_table=in_table,
        chars_width=chars_width,
    )
