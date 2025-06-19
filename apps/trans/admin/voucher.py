from django.contrib import admin
from django.http import HttpRequest
from import_export.admin import ImportExportModelAdmin

from .. import models  # , resources
from ..constants import vouchers as constants
from . import _actions

LIST_DISPLAY = (
    "voucher_serial",
    "title",
    "date",
    "total",
    "transactions_count",
    "kind",
    "is_audited",
    "is_migrated",
)
LIST_DISPLAY_LINKS = ("voucher_serial", "title")
LIST_PER_PAGE = 20
FIELDS = (
    ("voucher_serial", "created_at", "created_by"),
    ("updated_at", "updated_by"),
    ("is_audited", "audited_by", "is_deleted", "is_migrated"),
    ("title", "date"),
    ("kind", "period"),
    ("month", "quarter"),
    "notes",
    ("serial_id", "serial_date", "approve_date", "due_date"),
    "document",
    "accounting_journal_sequence",
)
READONLY_FIELDS = (
    "id",
    "uuid",
    "created_at",
    "updated_at",
    "created_by",
    "updated_by",
    "is_audited",
    "audited_by",
    "is_migrated",
    "is_deleted",
    "voucher_serial",
    "slug",
)


class VoucherAdminMixin:
    def has_migrate_voucher_permission(self, request: HttpRequest, obj=None):
        return request.user.has_perm("trans.migrate_voucher")

    def has_unmigrate_voucher_permission(self, request: HttpRequest, obj=None):
        return request.user.has_perm("trans.unmigrate_voucher")

    def has_audit_voucher_permission(self, request: HttpRequest, obj=None):
        return request.user.has_perm("trans.audit_voucher")

    def has_unaudit_voucher_permission(self, request: HttpRequest, obj=None):
        return request.user.has_perm("trans.unaudit_voucher")

    @admin.display(description="total")
    def total(self, obj: models.Voucher):
        return f"{obj.total:,.2f}"

    @admin.display(description="transactions count")
    def transactions_count(self, obj: models.Voucher):
        return obj.transactions_count


@admin.register(models.VoucherProxy)
class VoucherProxyAdmin(
    VoucherAdminMixin,
    ImportExportModelAdmin,
    admin.ModelAdmin,
):
    list_display = [*LIST_DISPLAY, "is_deleted"]
    search_fields = constants.SEARCH_FIELDS
    list_per_page = LIST_PER_PAGE
    fields = FIELDS
    readonly_fields = READONLY_FIELDS
    actions = (_actions.undo_delete,)

    def delete_model(self, request, obj):
        return obj.delete(permanent=True)


class VoucherTransactionInline(admin.TabularInline):
    parent_model = models.Voucher
    model = models.VoucherTransaction
    extra = 1
    fields = (
        "employee",
        "compensation",
        "quantity",
        "value",
    )
    ordering = ("-voucher__date", "voucher__voucher_serial")
    autocomplete_fields = ("employee", "compensation")


@admin.register(models.Voucher)
class VoucherAdmin(VoucherAdminMixin, ImportExportModelAdmin, admin.ModelAdmin):
    list_display = LIST_DISPLAY
    list_display_links = LIST_DISPLAY_LINKS
    search_fields = constants.SEARCH_FIELDS
    list_per_page = LIST_PER_PAGE
    fields = FIELDS
    readonly_fields = READONLY_FIELDS
    # resource_classes = (resources.VoucherResource,)
    inlines = (VoucherTransactionInline,)
    actions = (
        _actions.audit,
        _actions.unaudit,
        _actions.migrate,
        _actions.unmigrate,
        _actions.soft_delete,
    )

    def save_model(self, request, obj, form, change):
        if change:
            obj.is_audited = False
        else:
            obj.created_by = request.user

        obj.updated_by = request.user

        return super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=...):
        return False  # to remove Delete selected Vouchers action
