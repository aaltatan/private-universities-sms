from django.utils.translation import gettext as _


ORDERING_FIELDS: dict[str, str] = {
    "id": _("id").title(),
    "name": _("name").title(),
    "order": _("order").title(),
    "description": _("description").title(),
}

SEARCH_FIELDS: tuple[str] = ("name", "description")
