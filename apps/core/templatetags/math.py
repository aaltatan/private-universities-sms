from django import template


register = template.Library()


@register.filter
def multiply(value: int, arg: int) -> bool:
    return value * arg
