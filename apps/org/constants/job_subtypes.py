from django.utils.translation import gettext as _


ORDERING_FIELDS: dict[str, str] = {
    "id": _("id").title(),
    "name": _("name").title(),
    "job_type__name": _("job type").title(),
    "description": _("description").title(),
}

SEARCH_FIELDS: tuple[str] = ("name", "job_type", "description")
