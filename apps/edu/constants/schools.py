from django.utils.translation import gettext as _


ORDERING_FIELDS: dict[str, str] = {
    "id": _("id"),
    "name": _("name"),
    "kind__name": _("kind"),
    "nationality__name": _("nationality"),
    "website": _("website"),
    "email": _("email"),
    "phone": _("phone"),
    "description": _("description"),
}

SEARCH_FIELDS: tuple[str] = ("name", "kind__name", "description")
