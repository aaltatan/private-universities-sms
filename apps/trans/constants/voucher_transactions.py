from django.utils.translation import gettext as _


ORDERING_FIELDS: dict[str, str] = {
    "id": _("id"),
    "voucher__voucher_serial": _("voucher serial"),
    "voucher__date": _("voucher date"),
    "voucher__kind": _("voucher kind"),
    "employee__fullname": _("employee fullname"),
    "compensation__name": _("compensation name"),
    "ordering": _("ordering"),
}

SEARCH_FIELDS: tuple[str] = (
    "voucher__title",
    "voucher__voucher_serial",
    "employee__firstname",
    "compensation__name",
)
