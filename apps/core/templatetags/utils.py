import json
from typing import Any

from django import template
from django.db.models import Model

register = template.Library()


@register.filter
def get(value: Any, arg: str) -> Any:
    return getattr(value, arg, None)


@register.filter
def get_first_value(value: dict) -> Any:
    return list(value.values())[0]


@register.filter
def pretty_json(value):
    return json.dumps(value, indent=2, ensure_ascii=False)


@register.filter
def verbose_name(Klass: type[Model], field: str) -> str:
    return Klass._meta.get_field(field).verbose_name.title()
