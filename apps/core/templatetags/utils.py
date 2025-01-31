import json
from typing import Any

from django import template

register = template.Library()


@register.filter
def get(value: Any, arg: str) -> Any:
    return getattr(value, arg, None)


@register.filter
def pretty_json(value):
    return json.dumps(value, indent=2, ensure_ascii=False)
