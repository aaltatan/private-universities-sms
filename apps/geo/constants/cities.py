from django.utils.translation import gettext as _


ORDERING_FIELDS: dict[str, str] = {
    "id": _("id").title(),
    "name": _("name").title(),
    "governorate": _("governorate").title(),
    "description": _("description").title(),
}

SEARCH_FIELDS: tuple[str] = ("name", "governorate__name", "description")
