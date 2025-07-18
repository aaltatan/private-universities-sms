from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.utils import ActionBehavior

from .models import Voucher


class VoucherDeleter(ActionBehavior[Voucher]):
    success_obj_msg = _("voucher deleted successfully")
    error_obj_msg = _("you can't delete this voucher because it is migrated.")
    success_qs_msg = _("vouchers deleted successfully")
    error_qs_msg = _("you can't delete vouchers because they are migrated.")

    def check_obj_executing_possibility(self, obj) -> bool:
        return not obj.is_migrated

    def check_queryset_executing_possibility(self, qs) -> bool:
        return not qs.filter(is_migrated=True).exists()

    def action(self, **kwargs) -> tuple[int, dict[str, int]] | None:
        if self._kind == "obj":
            status = self.check_obj_executing_possibility(self._obj)
        elif self._kind == "qs":
            status = self.check_queryset_executing_possibility(self._obj)

        if not status:
            return self._handle_executing_error()

        self.has_executed = True

        if self._kind == "obj":
            self._obj.is_deleted = True
            self._obj.save()
        elif self._kind == "qs":
            self._obj.update(is_deleted=True)


class VoucherAuditor(ActionBehavior[Voucher]):
    success_obj_msg = _("voucher audited successfully")
    error_obj_msg = _(
        "you can't audit a voucher that you have created or updated or already has been audited or migrated"
    )
    success_qs_msg = _("vouchers audited successfully")
    error_qs_msg = _(
        "you can't audit vouchers that you have created or updated or already have been audited or migrated"
    )

    def check_obj_executing_possibility(self, obj) -> bool:
        if obj.is_audited or obj.is_migrated:
            return False
        return False if obj.updated_by == self.request.user else True

    def check_queryset_executing_possibility(self, qs) -> bool:
        if qs.filter(models.Q(is_audited=True) | models.Q(is_migrated=True)).exists():
            return False
        return not qs.filter(updated_by=self.request.user).exists()

    def action(self, **kwargs) -> tuple[int, dict[str, int]] | None:
        if self._kind == "obj":
            status = self.check_obj_executing_possibility(self._obj)
        elif self._kind == "qs":
            status = self.check_queryset_executing_possibility(self._obj)

        if not status:
            return self._handle_executing_error()

        self.has_executed = True

        if self._kind == "obj":
            self._obj.audit(self.request.user)
        else:
            self._obj.update(is_audited=True, audited_by=self.request.user)

        return


class VoucherMigrator(ActionBehavior[Voucher]):
    success_obj_msg = _("voucher migrated successfully")
    error_obj_msg = _("you can't migrate unaudited or migrated voucher")
    success_qs_msg = _("vouchers migrated successfully")
    error_qs_msg = _("you can't migrate unaudited or migrated vouchers")

    def check_obj_executing_possibility(self, obj) -> bool:
        if obj.is_migrated:
            return False
        return obj.is_audited

    def check_queryset_executing_possibility(self, qs) -> bool:
        return (
            False
            if qs.filter(
                models.Q(is_audited=False) | models.Q(is_migrated=True)
            ).exists()
            else True
        )

    def action(self, **kwargs) -> tuple[int, dict[str, int]] | None:
        if self._kind == "obj":
            status = self.check_obj_executing_possibility(self._obj)
        elif self._kind == "qs":
            status = self.check_queryset_executing_possibility(self._obj)

        if not status:
            return self._handle_executing_error()

        self.has_executed = True
        if self._kind == "obj":
            self._obj.migrate()
        else:
            queryset = self._obj
            for obj in queryset:
                obj.migrate()

        return


class VoucherUnMigrator(ActionBehavior[Voucher]):
    success_obj_msg = _("voucher unmigrated successfully")
    error_obj_msg = _("you can't unmigrate unmigrated voucher")
    success_qs_msg = _("vouchers migrated successfully")
    error_qs_msg = _("you can't unmigrate unmigrated vouchers")

    def check_obj_executing_possibility(self, obj) -> bool:
        return obj.is_migrated

    def check_queryset_executing_possibility(self, qs) -> bool:
        if qs.filter(is_migrated=False).exists():
            return False
        return qs.filter(is_migrated=True).exists()

    def action(self) -> tuple[int, dict[str, int]] | None:
        if self._kind == "obj":
            status = self.check_obj_executing_possibility(self._obj)
        elif self._kind == "qs":
            status = self.check_queryset_executing_possibility(self._obj)

        if not status:
            return self._handle_executing_error()

        self.has_executed = True

        if self._kind == "obj":
            self._obj.unmigrate()
        else:
            queryset = self._obj
            for obj in queryset:
                obj.unmigrate()

        return
