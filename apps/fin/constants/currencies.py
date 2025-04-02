from django.utils.translation import gettext as _


ORDERING_FIELDS: dict[str, str] = {
    "id": _("id"),
    "name": _("name"),
    "symbol": _("symbol"),
    "code": _("code"),
    "fraction_name": _("fraction name"),
    "is_primary": _("is primary"),
    "description": _("description"),
}

SEARCH_FIELDS: tuple[str] = ("name", "description")
