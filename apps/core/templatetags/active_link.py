from django import template
from django.http import HttpRequest
from django.utils.encoding import escape_uri_path


register = template.Library()


@register.simple_tag(takes_context=True)
def active_link(
    context,
    path: str,
    css_active_text: str = "active",
    css_inactive_text: str = "",
):

    request: HttpRequest | None = context.get("request")
    if request is None:
        # Can't work without the request object.
        return css_inactive_text

    active = False
    request_path = escape_uri_path(request.path)

    if request_path == path == "/":
        active = True
    else:
        path = path[1:]
        request_path = request_path[1:]
        if path:
            active = request_path.startswith(path)

    if active:
        return css_active_text

    return css_inactive_text
