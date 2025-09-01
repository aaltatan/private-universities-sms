from django.utils.translation import gettext_lazy as _


ORDERING_FIELDS: dict[str, str] = {
    "id": _("id"),
    "tax": _("tax"),
    "amount_from": _("amount from"),
    "amount_to": _("amount to"),
    "rate": _("rate"),
    "notes": _("notes"),
}

SEARCH_FIELDS: tuple[str] = ("tax__name",)
