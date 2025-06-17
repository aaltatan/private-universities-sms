from django.utils.translation import gettext_lazy as _
from django.db.models import ProtectedError

from apps.core.utils import ActionBehavioral

from .models import Voucher


class VoucherDeleter(ActionBehavioral[Voucher]):
    success_obj_msg = _("voucher deleted successfully")
    error_obj_msg = _(
        "you can't delete this voucher because it is related to other objects."
    )
    success_qs_msg = _("vouchers deleted successfully")
    error_qs_msg = _(
        "you can't delete vouchers because they are related to other objects."
    )

    def check_obj_executing_possibility(self, obj) -> bool:
        return not obj.is_migrated

    def check_queryset_executing_possibility(self, qs) -> bool:
        return not qs.filter(is_migrated=True).exists()

    def action(self) -> tuple[int, dict[str, int]] | None:
        if self._kind == "obj":
            status = self.check_obj_executing_possibility(self._obj)
        elif self._kind == "qs":
            status = self.check_queryset_executing_possibility(self._obj)

        if not status:
            return self._handle_executing_error()

        try:
            self.has_executed = True
            self._obj.is_deleted = True
            return
        except ProtectedError:
            self._handle_executing_error()


class VoucherAuditor(ActionBehavioral[Voucher]):
    success_obj_msg = _("voucher audited successfully")
    error_obj_msg = _(
        "you can't audit your the vouchers that you have created or updated"
    )
    success_qs_msg = _("vouchers audited successfully")
    error_qs_msg = _(
        "you can't audit your the vouchers that you have created or updated"
    )

    def check_obj_executing_possibility(self, obj) -> bool:
        return obj.updated_by != self.request.user

    def check_queryset_executing_possibility(self, qs) -> bool:
        return not qs.filter(updated_by=self.request.user).exists()

    def action(self) -> tuple[int, dict[str, int]] | None:
        if self._kind == "obj":
            status = self.check_obj_executing_possibility(self._obj)
        elif self._kind == "qs":
            status = self.check_queryset_executing_possibility(self._obj)

        if not status:
            return self._handle_executing_error()

        self.has_executed = True

        if self._kind == "obj":
            self._obj.is_audited = True
            self._obj.audited_by = self.request.user
        else:
            self._obj.update(is_audited=True, audited_by=self.request.user)

        return
