from decimal import Decimal

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


def format_string(
    value: str,
    chars_width: int = 15,
    in_table: bool = False,
) -> str:
    right_result = value.rjust(chars_width)
    left_result = value.ljust(chars_width)
    if in_table:
        return mark_safe(
            f"""
            <pre class='rtl:hidden font-medium'>{right_result}</pre>
            <pre class='ltr:hidden font-medium'>{left_result}</pre>
            """,
        )
    else:
        return mark_safe(f"<pre class='font-medium'>{value}</pre>")


@register.filter
def percentage(
    value: float | Decimal | int,
    in_table: bool = False,
    decimal_places: int = 2,
) -> str:
    result = f"{value * 100:.{decimal_places}f} %"
    return format_string(result, in_table=in_table, chars_width=10)


@register.filter
def money(
    value: float | Decimal | int,
    in_table: bool = False,
    chars_width: int = 15,
) -> str:
    result = f"{value:,}"
    return format_string(result, in_table=in_table, chars_width=chars_width)
