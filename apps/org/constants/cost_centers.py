from django.utils.translation import gettext_lazy as _


ORDERING_FIELDS: dict[str, str] = {
    "id": _("id"),
    "name": _("name"),
    "accounting_id": _("accounting id"),
    "description": _("description"),
}

SEARCH_FIELDS: tuple[str] = ("name", "description")
