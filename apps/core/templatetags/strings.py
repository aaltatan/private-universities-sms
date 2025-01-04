from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter
@stringfilter
def startswith(value: str, arg: str) -> bool:
    return value.startswith(arg)


@register.filter
@stringfilter
def endswith(value: str, arg: str) -> bool:
    return value.endswith(arg)