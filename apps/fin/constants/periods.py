from django.utils.translation import gettext_lazy as _


ORDERING_FIELDS: dict[str, str] = {
    "id": _("id"),
    "name": _("name"),
    "year": _("year"),
    "start_date": _("start date"),
    "is_closed": _("is closed"),
    "description": _("description"),
}

SEARCH_FIELDS: tuple[str] = ("name", "year", "description")
