from typing import Any, Literal
from abc import ABC, abstractmethod

from django.db.models import QuerySet
from django.utils.translation import gettext as _


class Deleter(ABC):
    obj_success_message: str = _(
        "{} has been deleted successfully.",
    )
    qs_success_message: str = _(
        "all selected {} objects have been deleted successfully.",
    )
    obj_error_message: str = _(
        "{} cannot be deleted.",
    )
    qs_error_message: str = _(
        "selected {} objects cannot be deleted.",
    )

    def __init__(self, obj: Any):
        self.obj = obj

    @abstractmethod
    def is_obj_deletable(self) -> bool:
        """
        Returns whether the object can be deleted or not.
        you can use self.obj to get the object.
        """
        pass

    @abstractmethod
    def is_qs_deletable(self, qs: QuerySet) -> bool:
        """
        Returns whether the QuerySet can be deleted or not.
        you can use self.obj to get the QuerySet.
        """
        pass

    def is_deletable(self) -> bool:
        """
        Deletes the object.
        """
        if isinstance(self.obj, QuerySet):
            return self.is_qs_deletable(self.obj)
        else:
            return self.is_obj_deletable()

    def delete(self) -> None:
        self.obj.delete()

    def get_message(self, placeholder: str) -> str:
        obj_type = "qs" if isinstance(self.obj, QuerySet) else "obj"
        status = "success" if self.is_deletable() else "error"
        return self.__get_message(obj_type, status, placeholder)

    def __get_message(
        self,
        obj_type: Literal["obj", "qs"],
        status: Literal["success", "error"],
        placeholder: str,
    ) -> str:
        messages: dict[str, dict[str, str]] = {
            "obj": {
                "success": self.obj_success_message.format(
                    placeholder,
                ),
                "error": self.obj_error_message.format(
                    placeholder,
                ),
            },
            "qs": {
                "error": self.qs_error_message.format(
                    placeholder,
                ),
                "success": self.qs_success_message.format(
                    placeholder,
                ),
            },
        }
        return messages[obj_type][status]
