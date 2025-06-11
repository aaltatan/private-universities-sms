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
    )
    fields = (
        ("created_at", "updated_at"),
        "voucher",
        ("employee", "compensation"),
        ("quantity", "value", "tax"),
    )
    list_display_links = ("voucher",)
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
