from django.utils.translation import gettext as _


ORDERING_FIELDS: dict[str, str] = {
    "id": _("id"),
    "name": _("name"),
    "is_governmental": _("is governmental"),
    "is_virtual": _("is virtual"),
    "nationality__name": _("nationality"),
    "website": _("website"),
    "email": _("email"),
    "phone": _("phone"),
    "description": _("description"),
}

SEARCH_FIELDS: tuple[str] = ("name", "description")
