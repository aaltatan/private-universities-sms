from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Sequence

from django.db.models import QuerySet
from django.http import HttpResponse, HttpRequest
from django.utils.translation import gettext as _
from django.contrib import messages

from .constants import PERMISSION


@dataclass
class Perm:
    app_label: str
    permission: PERMISSION = "view"
    object_name: str | None = None

    def __post_init__(self) -> None:
        if self.object_name is None:
            if self.app_label.endswith("ies"):
                self.object_name = self.app_label[:-3] + "y"
                self.object_name = self.object_name.replace("_", "")
                return
            elif self.app_label.endswith("s"):
                self.object_name = self.app_label[:-1]
                self.object_name = self.object_name.replace("_", "")
                return
        else:
            self.object_name = self.object_name.replace("_", "")

    def __str__(self) -> str:
        return f"{self.app_label}.{self.permission}_{self.object_name}"

    @property
    def string(self) -> str:
        return str(self)


@dataclass
class Action:
    method: Callable[[QuerySet, dict], HttpResponse]
    template: str
    kwargs: Sequence[str] = field(default_factory=list)
    permissions: Sequence[Perm | str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if len(self.permissions) == 0:
            return

        if isinstance(self.permissions[0], Perm):
            self.permissions = [perm.string for perm in self.permissions]


class Deleter(ABC):
    def __init__(
        self,
        obj,
        request: HttpRequest | None = None,
        send_success_messages: bool = True,
        send_error_messages: bool = True,
    ) -> None:
        self.obj = obj
        self.request = request
        self.send_success_messages = send_success_messages
        self.send_error_messages = send_error_messages

        if self.request is None and (
            self.send_success_messages or self.send_error_messages
        ):
            raise AttributeError(
                "you must provide a request object.",
            )

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

    def get_obj_success_message(self, obj: Any):
        return _("{} has been deleted successfully").format(obj)

    def get_obj_error_message(self, obj: Any):
        return _(
            "you can't delete ({}) because there is one or more models related to it.",
        ).format(obj)

    def get_qs_success_message(
        self,
        deleted_objects: tuple[int, dict[str, str]],
    ):
        return _(
            "all ({}) selected objects have been deleted successfully",
        ).format(deleted_objects[0])

    def get_qs_error_message(self, obj: QuerySet):
        return _(
            "you can't delete these ({}) selected objects because there is one or more related to other objects.",
        ).format(obj.count())

    def __error_scenario(self) -> None:
        if self.send_error_messages:
            if isinstance(self.obj, QuerySet):
                messages.error(
                    self.request,
                    self.get_qs_error_message(self.obj),
                )
            else:
                messages.error(
                    self.request,
                    self.get_obj_error_message(self.obj),
                )

    def __success_scenario(self) -> None:
        if isinstance(self.obj, QuerySet):
            deleted_objects = self.obj.all().delete()
            if self.send_success_messages:
                messages.success(
                    self.request,
                    self.get_qs_success_message(deleted_objects),
                )
        else:
            self.obj.delete()
            if self.send_success_messages:
                messages.success(
                    self.request,
                    self.get_obj_success_message(self.obj),
                )

    def delete(self) -> bool:
        if isinstance(self.obj, QuerySet):
            is_deletable = self.is_qs_deletable(self.obj)
        else:
            is_deletable = self.is_obj_deletable()

        if is_deletable:
            self.__success_scenario()
        else:
            self.__error_scenario()

        return is_deletable
