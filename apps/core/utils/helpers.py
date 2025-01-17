from dataclasses import dataclass, field
from typing import Callable, Sequence

from django.db.models import QuerySet
from django.http import HttpResponse

from ..constants import PERMISSION


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
