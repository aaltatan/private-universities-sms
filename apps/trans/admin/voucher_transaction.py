from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .. import models  # , resources
from ..constants import vouchers as constants


@admin.register(models.VoucherTransaction)
class VoucherTransactionAdmin(
    ImportExportModelAdmin,
    admin.ModelAdmin,
):
    list_display = (
        "voucher",
        "voucher__date",
        "employee",
        "compensation",
        "quantity",
        "formatted_value",
        "total",
        "formatted_tax",
        "net",
        "ordering",
        "voucher__is_audited",
        "voucher__is_migrated",
        "voucher__is_deleted",
    )
    fields = (
        ("voucher", "created_at", "updated_at"),
        ("employee", "compensation"),
        ("quantity", "value", "tax"),
        ("notes",),
    )
    list_display_links = ("voucher",)
    list_filter = ("voucher__voucher_serial",)
    search_fields = constants.SEARCH_FIELDS
    autocomplete_fields = ("employee", "compensation", "voucher")
    list_per_page = 20
    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
        "slug",
        "tax",
        "ordering",
        "voucher",
    )
    # resource_classes = (resources.VoucherResource,)

    @admin.display(description="value")
    def formatted_value(self, obj: models.VoucherTransaction):
        return f"{obj.value:,.2f}"

    @admin.display(description="tax")
    def formatted_tax(self, obj: models.VoucherTransaction):
        return f"{obj.tax:,.2f}"

    @admin.display(description="total")
    def total(self, obj: models.VoucherTransaction):
        return f"{obj.total:,.2f}"

    @admin.display(description="net")
    def net(self, obj: models.VoucherTransaction):
        return f"{obj.net:,.2f}"
