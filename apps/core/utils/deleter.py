from typing import Literal, Generic, TypeVar

from django.db.models import ProtectedError, QuerySet, Model
from django.utils.translation import gettext as _

KIND = Literal["obj", "qs"]
STATUS = Literal["success", "error"]


T = TypeVar("T", bound=Model)


class Deleter(Generic[T]):
    """
    A class that handles the deletion of objects.
    """

    success_qs_msg: str | None = None
    error_qs_msg: str | None = None
    success_obj_msg: str | None = None
    error_obj_msg: str | None = None

    def __init__(
        self,
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

        self.has_deleted = False
        self._kind: KIND = "obj"
        self._status: STATUS = "success"
        self._count = 0

        if obj is None:
            self._obj = queryset
            self._kind = "qs"
        else:
            self._obj = obj

    def check_obj_deleting_possibility(self, obj: T) -> bool:
        """
        Hook for doing any extra not delete reasoning before deleting the object.
        """
        return True

    def check_queryset_deleting_possibility(self, qs: QuerySet) -> bool:
        """
        Hook for doing any extra not delete reasoning before deleting the queryset.
        """
        return True

    def delete(self) -> tuple[int, dict[str, int]] | None:

        if self._kind == "obj":
            status = self.check_obj_deleting_possibility(self._obj)
        elif self._kind == "qs":
            status = self.check_queryset_deleting_possibility(self._obj)

        if not status:
            return self._handle_deleting_error()

        try:
            self.has_deleted = True
            deleted_obj = self._obj.delete()
            self._count, _ = deleted_obj
            return deleted_obj
        except ProtectedError:
            self._handle_deleting_error()

    def get_message(self) -> str:
        if self._kind == "obj" and self._status == "success":
            return self._messages["obj"]["success"].format(self._obj)

        if self._kind == "obj" and self._status == "error":
            return self._messages["obj"]["error"].format(self._obj)

        if self._kind == "qs" and self._status == "success":
            return self._messages["qs"]["success"]

        if self._kind == "qs" and self._status == "error":
            return self._messages["qs"]["error"]

    def _handle_deleting_error(self) -> None:
        self.has_deleted = False
        self._status = "error"
        return

    @property
    def _messages(self) -> dict[KIND, dict[STATUS, str]]:
        return {
            "obj": {
                "success": self.success_obj_msg
                or _("{} has been deleted successfully."),
                "error": self.error_obj_msg or _("{} cannot be deleted."),
            },
            "qs": {
                "success": self.success_qs_msg
                or _(
                    "{} selected objects have been deleted successfully.".format(
                        self._count
                    ),
                ),
                "error": self.error_qs_msg
                or _(
                    "selected objects CANNOT be deleted because they are related to other objects.",
                ),
            },
        }
