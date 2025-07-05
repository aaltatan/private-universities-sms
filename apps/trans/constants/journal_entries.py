from django.utils.translation import gettext as _


ORDERING_FIELDS: dict[str, str] = {
    "id": _("id"),
}

SEARCH_FIELDS: tuple[str] = (
    "cost_center__name",
    "voucher__title",
    "period__year__name",
    "period__name",
    "voucher__voucher_serial",
    "employee__fullname",
    "tax__name",
    "compensation__name",
)
