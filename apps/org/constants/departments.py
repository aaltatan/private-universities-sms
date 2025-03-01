from django.utils.translation import gettext as _


ORDERING_FIELDS: dict[str, str] = {
    "id": _("id"),
    "name": _("name"),
    "cost_center__name": _("cost center"),
    "description": _("description"),
}

SEARCH_FIELDS: tuple[str] = ("name", "description")
