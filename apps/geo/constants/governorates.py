from django.utils.translation import gettext as _


ORDERING_FIELDS: dict[str, str] = {
    "id": _("id"),
    "name": _("name"),
    "cities_count": _("cities count"),
    "description": _("description"),
}

SEARCH_FIELDS: tuple[str] = ("name", "description")
