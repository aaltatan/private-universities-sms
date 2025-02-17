from django.utils.translation import gettext as _


ORDERING_FIELDS: dict[str, str] = {
    "id": _("id"),
    "name": _("name"),
    "governorate": _("governorate"),
    "description": _("description"),
}

SEARCH_FIELDS: tuple[str] = ("name", "governorate__name", "description")
