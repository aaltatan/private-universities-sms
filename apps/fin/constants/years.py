from django.utils.translation import gettext_lazy as _


ORDERING_FIELDS: dict[str, str] = {
    "id": _("id"),
    "name": _("name"),
    "description": _("description"),
}

SEARCH_FIELDS: tuple[str] = ("name", "description")
