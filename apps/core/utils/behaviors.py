from typing import Literal, Generic, TypeVar

from django.http import HttpRequest
from django.db.models import ProtectedError, QuerySet, Model
from django.utils.translation import gettext as _

KIND = Literal["obj", "qs"]
STATUS = Literal["success", "error"]


T = TypeVar("T", bound=Model)


class ActionBehavior(Generic[T]):
    """
    A class that handles the deletion of objects.
    """

    success_qs_msg: str | None = None
    error_qs_msg: str | None = None
    success_obj_msg: str | None = None
    error_obj_msg: str | None = None

    def __init__(
        self,
        request: HttpRequest | None = None,
        obj: T | None = None,
        queryset: QuerySet | None = None,
    ):
        if obj is None and queryset is None:
            raise ValueError(
                "obj or queryset must be provided.",
            )

        if obj is not None and queryset is not None:
            raise ValueError(
                "obj and queryset cannot be provided at the same time.",
            )

        if queryset is not None and not isinstance(queryset, QuerySet):
            raise ValueError(
                "queryset must be a QuerySet instance.",
            )

        self.request = request
        self.has_executed = False
        self._kind: KIND = "obj"
        self._status: STATUS = "success"
        self._count = 0

        if obj is None:
            self._obj = queryset
            self._kind = "qs"
        else:
            self._obj = obj

    def check_obj_executing_possibility(self, obj: T) -> bool:
        """
        Hook for doing any extra not executing reasoning before executing on the object.
        """
        return True

    def check_queryset_executing_possibility(self, qs: QuerySet) -> bool:
        """
        Hook for doing any extra not executing reasoning before executing the queryset.
        """
        return True

    def action(self) -> tuple[int, dict[str, int]] | None:
        raise NotImplementedError

    def get_message(self) -> str:
        if self._kind == "obj" and self._status == "success":
            return self._messages["obj"]["success"].format(self._obj)

        if self._kind == "obj" and self._status == "error":
            return self._messages["obj"]["error"].format(self._obj)

        if self._kind == "qs" and self._status == "success":
            return self._messages["qs"]["success"]

        if self._kind == "qs" and self._status == "error":
            return self._messages["qs"]["error"]

    def _handle_executing_error(self) -> None:
        self.has_executed = False
        self._status = "error"
        return

    @property
    def _messages(self) -> dict[KIND, dict[STATUS, str]]:
        return {
            "obj": {
                "success": self.success_obj_msg or _("done"),
                "error": self.error_obj_msg or _("the operation was not completed."),
            },
            "qs": {
                "success": self.success_qs_msg or _("done"),
                "error": self.error_qs_msg or _("the operation was not completed."),
            },
        }


class Deleter(ActionBehavior[T]):
    success_obj_msg = _("object has been deleted successfully.")
    error_obj_msg = _(
        "you can't delete this object because it is related to other objects."
    )
    success_qs_msg = _("objects have been deleted successfully.")
    error_qs_msg = _(
        "you can't delete objects because they are related to other objects."
    )

    def action(self) -> tuple[int, dict[str, int]] | None:
        if self._kind == "obj":
            status = self.check_obj_executing_possibility(self._obj)
        elif self._kind == "qs":
            status = self.check_queryset_executing_possibility(self._obj)

        if not status:
            return self._handle_executing_error()

        try:
            self.has_executed = True
            deleted_obj = self._obj.delete()
            self._count, _ = deleted_obj
            return deleted_obj
        except ProtectedError:
            self._handle_executing_error()
