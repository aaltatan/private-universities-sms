from django.utils.translation import gettext as _


ORDERING_FIELDS: dict[str, str] = {
    "id": _("id"),
    "name": _("name"),
    "is_local": _("locality"),
    "description": _("description"),
    "employees_count": _("employees count"),
}

SEARCH_FIELDS: tuple[str] = ("name", "description")
