from django.utils.translation import gettext_lazy as _


ORDERING_FIELDS: dict[str, str] = {
    "id": _("id"),
    "name": _("name"),
    "is_payable": _("payable"),
    "is_separated": _("separated"),
    "description": _("description"),
}

SEARCH_FIELDS: tuple[str] = ("name", "description")
