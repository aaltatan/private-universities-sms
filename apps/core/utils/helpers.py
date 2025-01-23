from dataclasses import dataclass, field, InitVar
from typing import Callable, Sequence

from django.db.models import QuerySet
from django.http import HttpResponse, HttpRequest, Http404

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


@dataclass
class AutocompleteRequestParser:
    request: InitVar[HttpRequest]
    app_label: str = field(init=False)
    model_name: str = field(init=False)
    object_name: str = field(init=False)
    field_name: str = field(init=False)
    term: str = field(init=False)

    def __post_init__(self, request: HttpRequest):
        self.app_label = request.GET.get("app_label", "")
        if not self.app_label:
            raise Http404("app_label is required")

        self.model_name = request.GET.get("model_name", "").lower()
        if not self.model_name:
            raise Http404("model_name is required")

        self.object_name = request.GET.get("object_name", "").lower()
        if not self.object_name:
            raise Http404("object_name is required")

        self.field_name = request.GET.get("field_name", "")
        if not self.field_name:
            raise Http404("field_name is required")

        self.term = request.GET.get("term", "")
