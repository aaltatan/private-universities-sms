from typing import Any

from django import template


register = template.Library()


@register.filter
def get(value: Any, arg: str) -> Any:
    return getattr(value, arg, None)