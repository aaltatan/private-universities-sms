from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .. import models
from ..constants import journal_entries as constants


@admin.register(models.JournalEntry)
class JournalEntryAdmin(
    ImportExportModelAdmin,
    admin.ModelAdmin,
):
    list_display = (
        "employee",
        "formatted_debit",
        "formatted_credit",
        "fiscal_object",
        "cost_center",
        "date",
        "period",
        "month",
        "voucher",
        "general_serial",
        "ordering",
    )
    fields = (
        ("uuid", "created_at", "updated_at"),
        ("date", "month", "quarter", "period"),
        ("debit", "credit"),
        ("employee", "cost_center"),
        ("content_type", "fiscal_object_id", "fiscal_object"),
        "voucher",
        ("explanation", "notes"),
    )
    search_fields = constants.SEARCH_FIELDS
    autocomplete_fields = ("employee", "voucher", "cost_center", "period")
    list_per_page = 20

    @admin.display(description="debit")
    def formatted_debit(self, obj: models.JournalEntry):
        return f"{obj.debit:,.2f}"

    @admin.display(description="credit")
    def formatted_credit(self, obj: models.JournalEntry):
        return f"{obj.credit:,.2f}"

    def has_change_permission(self, request, obj=None):
        return False
