from django.utils.translation import gettext as _


ORDERING_FIELDS: dict[str, str] = {
    "id": _("id"),
    "name": _("name"),
    "order": _("order"),
    "is_academic": _("is academic"),
    "description": _("description"),
}

SEARCH_FIELDS: tuple[str] = ("name", "description")
