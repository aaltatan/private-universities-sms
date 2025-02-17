from django.utils.translation import gettext as _


ORDERING_FIELDS: dict[str, str] = {
    "id": _("id"),
    "name": _("name"),
    "job_type__name": _("job type"),
    "description": _("description"),
}

SEARCH_FIELDS: tuple[str] = ("name", "job_type__name", "description")
