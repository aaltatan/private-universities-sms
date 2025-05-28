from decimal import Decimal

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def percentage(value: float | Decimal | int, decimal_places: int = 2) -> str:
    result = f"{value * 100:.{decimal_places}f} %"
    right_result = result.rjust(10)
    left_result = result.ljust(10)
    return mark_safe(
        f"""
        <pre class='rtl:hidden font-medium'>{right_result}</pre>
        <pre class='ltr:hidden font-medium'>{left_result}</pre>
        """,
    )


@register.filter
def money(value: float | Decimal | int, chars_width: int = 15) -> str:
    result = f"{value:,}"
    right_result = result.rjust(chars_width)
    left_result = result.ljust(chars_width)
    return mark_safe(
        f"""
        <pre class='rtl:hidden font-medium'>{right_result}</pre>
        <pre class='ltr:hidden font-medium'>{left_result}</pre>
        """,
    )
