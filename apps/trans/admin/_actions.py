from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


@admin.action(description="Undo delete selected vouchers")
def undo_delete(modeladmin: ModelAdmin, request: HttpRequest, qs: QuerySet):
    qs.update(is_deleted=False)
    message = _("vouchers undeleted successfully").title()
    modeladmin.message_user(request, message, level=messages.SUCCESS)


@admin.action(description="Delete selected Vouchers (SOFT)")
def soft_delete(modeladmin: ModelAdmin, request: HttpRequest, qs: QuerySet):
    qs.update(is_deleted=True)
    message = _("vouchers deleted successfully").title()
    modeladmin.message_user(request, message, level=messages.SUCCESS)


@admin.action(
    description="Migrate selected Vouchers",
    permissions=["migrate_voucher"],
)
def migrate(modeladmin: ModelAdmin, request: HttpRequest, qs: QuerySet):
    if request.POST.get("post"):
        if qs.filter(is_audited=False).exists():
            message = _("cannot migrate vouchers that are not audited").title()
            modeladmin.message_user(request, message, level=messages.ERROR)
            return

        journal_sequence = request.POST.get("accounting_journal_sequence", "")
        qs.update(
            is_migrated=True,
            accounting_journal_sequence=journal_sequence,
        )
        message = _("vouchers migrated successfully").title()
        modeladmin.message_user(request, message, level=messages.SUCCESS)
        return

    return render(
        request,
        "admin/migration-confirmation.html",
        {
            "title": _("migrate selected vouchers"),
            "objects": qs,
            "action_checkbox_name": admin.helpers.ACTION_CHECKBOX_NAME,
        },
    )


@admin.action(
    description="Unmigrate selected Vouchers",
    permissions=["unmigrate_voucher"],
)
def unmigrate(modeladmin: ModelAdmin, request: HttpRequest, qs: QuerySet):
    qs.update(is_migrated=False, accounting_journal_sequence="")
    message = _("vouchers unmigrated successfully").title()
    modeladmin.message_user(request, message, level=messages.SUCCESS)


@admin.action(
    description="Audit selected Vouchers",
    permissions=["audit_voucher"],
)
def audit(modeladmin: ModelAdmin, request: HttpRequest, qs: QuerySet):
    if qs.filter(updated_by=request.user).exists():
        message = _(
            "you can't audit your the vouchers that you have created or updated"
        ).title()
        modeladmin.message_user(request, message, level=messages.ERROR)
        return

    qs.update(is_audited=True, audited_by=request.user)
    message = _("vouchers audited successfully").title()
    modeladmin.message_user(request, message, level=messages.SUCCESS)


@admin.action(
    description="Unaudit selected Vouchers",
    permissions=["unaudit_voucher"],
)
def unaudit(modeladmin: ModelAdmin, request: HttpRequest, qs: QuerySet):
    qs.update(is_audited=False)
    message = _("vouchers unaudited successfully").title()
    modeladmin.message_user(request, message, level=messages.SUCCESS)
