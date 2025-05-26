from decimal import Decimal

from django import template

register = template.Library()


@register.filter
def percentage(value: float | Decimal | int, decimal_places: int = 2) -> str:
    return f"{value * 100:.{decimal_places}f}%"
