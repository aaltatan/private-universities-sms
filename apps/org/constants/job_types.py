from django.utils.translation import gettext as _


ORDERING_FIELDS: dict[str, str] = {
    "id": _("id"),
    "name": _("name"),
    "job_subtypes_count": _("job subtypes count"),
    "description": _("description"),
}

SEARCH_FIELDS: tuple[str] = ("name", "description")
