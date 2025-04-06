from django.utils.translation import gettext as _

ORDERING_FIELDS: dict[str, str] = {
    "id": _("id"),
    "currency__name": _("currency"),
    "currency__is_primary": _("is primary"),
    "created_at": _("created at"),
    "date": _("date"),
    "rate": _("rate"),
    "notes": _("notes"),
}

SEARCH_FIELDS: tuple[str] = ("currency__name", "notes")
