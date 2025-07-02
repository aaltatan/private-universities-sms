from django.utils.translation import gettext as _


ORDERING_FIELDS: dict[str, str] = {
    "id": _("id"),
}

SEARCH_FIELDS: tuple[str] = (
    "voucher__title",
    "voucher__voucher_serial",
    "employee__fullname",
)
