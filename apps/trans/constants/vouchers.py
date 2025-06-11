from django.utils.translation import gettext as _


ORDERING_FIELDS: dict[str, str] = {
    "id": _("id"),
    "voucher_serial": _("voucher serial"),
    "title": _("title"),
    "date": _("date"),
    "kind": _("kind"),
    "month": _("month"),
    "quarter": _("quarter"),
    "period": _("period"),
    "notes": _("notes"),
    "serial_id": _("serial id"),
    "serial_date": _("serial date"),
    "approve_date": _("approve date"),
    "due_date": _("due date"),
    "accounting_journal_sequence": _("accounting journal sequence"),
    "is_audited": _("is audited"),
    "is_migrated": _("is migrated"),
}

SEARCH_FIELDS: tuple[str] = (
    "title",
    "voucher_serial",
    "month",
    "period__name",
    "notes",
)
