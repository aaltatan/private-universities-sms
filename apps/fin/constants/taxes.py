from django.utils.translation import gettext as _


ORDERING_FIELDS: dict[str, str] = {
    "id": _("id"),
    "name": _("name"),
    "calculation_method": _("calculation method"),
    "description": _("description"),
}

SEARCH_FIELDS: tuple[str] = ("name", "description")
