from django.utils.translation import gettext as _


ORDERING_FIELDS: dict[str, str] = {
    "id": _("id"),
    "name": _("name"),
    "shortname": _("short name"),
    "calculation_method": _("calculation method"),
    "tax": _("tax"),
    "tax_classification": _("tax classification"),
    "value": _("value"),
    "min_value": _("min value"),
    "max_value": _("max value"),
    "affected_by_working_days": _("affected by working days"),
    "is_active": _("is active"),
    "accounting_id": _("accounting id"),
    "description": _("description"),
}

SEARCH_FIELDS: tuple[str] = ("name", "description")
