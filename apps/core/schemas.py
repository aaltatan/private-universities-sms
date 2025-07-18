import json
from dataclasses import InitVar, asdict, dataclass, field
from typing import Any, Literal, Sequence

from django.http import Http404, HttpRequest
from rest_framework.response import Response

from apps.core.utils.behaviors import ActionBehavior

from .constants import PERMISSION
from .forms import BehaviorForm


@dataclass
class AppLink:
    icon: str
    text: str
    path: str
    perm: str | None = None

    def asdict(self) -> dict[str, str]:
        return asdict(self)


@dataclass
class Perm:
    """A dataclass that represents a permission."""

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
    """A dataclass that represents an action."""

    behavior: type[ActionBehavior]
    template: str
    permissions: Sequence[Perm | str] = field(default_factory=list)
    form_class: type[BehaviorForm] | None = None

    def __post_init__(self) -> None:
        if len(self.permissions) == 0:
            return

        if isinstance(self.permissions[0], Perm):
            self.permissions = [perm.string for perm in self.permissions]


@dataclass
class RequestParser:
    """A dataclass that represents the required data from http request."""

    request: InitVar[HttpRequest]
    index_url: str
    action: Literal["create", "update"]
    is_modal_request: bool = field(init=False)
    next_url: str = field(init=False, default="")
    target: str = field(init=False, default="")
    dont_redirect: bool = field(init=False)
    hx_location: str = field(init=False)
    querystring: str = field(init=False)
    save: bool = field(init=False, default=False)
    save_and_add_another: bool = field(init=False, default=False)
    save_and_continue_editing: bool = field(init=False, default=False)
    update: bool = field(init=False, default=False)
    update_and_continue_editing: bool = field(init=False, default=False)

    def __post_init__(self, request: HttpRequest):
        if request.method == "POST":
            if self.action == "create":
                self.save = request.POST.get("save") is not None
                self.save_and_add_another = (
                    request.POST.get("save_and_add_another") is not None
                )
                self.save_and_continue_editing = (
                    request.POST.get("save_and_continue_editing") is not None
                )
                if all(
                    [
                        self.save,
                        self.save_and_add_another,
                        self.save_and_continue_editing,
                    ]
                ):
                    raise ValueError(
                        "save, save_and_add_another and save_and_continue_editing are mutually exclusive"
                    )
                if (
                    not self.save
                    and not self.save_and_add_another
                    and not self.save_and_continue_editing
                ):
                    raise ValueError(
                        "save, save_and_add_another or save_and_continue_editing is required",
                    )
            elif self.action == "update":
                self.update = request.POST.get("update") is not None
                self.update_and_continue_editing = (
                    request.POST.get("update_and_continue_editing") is not None
                )
                if self.update and self.update_and_continue_editing:
                    raise ValueError(
                        "update and update_and_continue_editing are mutually exclusive"
                    )
                if not self.update and not self.update_and_continue_editing:
                    raise ValueError(
                        "update or update_and_continue_editing is required",
                    )

        self.is_modal_request = request.headers.get("modal") is not None

        self.target = request.headers.get("target")
        if not self.target and self.is_modal_request:
            raise ValueError("target is required")

        self.dont_redirect = request.headers.get("dont-redirect") is not None

        querystring = request.GET.urlencode()
        self.querystring = querystring and f"?{querystring}"
        self.index_url += self.querystring

        self.next_url = request.headers.get("referer", self.index_url)

        self.hx_location = json.dumps(
            {"path": self.next_url, "target": self.target},
        )

    def asdict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AutocompleteRequestParser:
    """A dataclass that parses the request for autocomplete views."""

    request: HttpRequest
    app_label: str = field(init=False)
    model_name: str = field(init=False)
    object_name: str = field(init=False)
    field_name: str = field(init=False)
    label_field_name: str = field(init=False)
    term: str = field(init=False)
    view_perm: str = field(init=False)

    def __post_init__(self):
        self.app_label = self.request.GET.get("app_label", "")
        if not self.app_label:
            raise AttributeError("app_label is required")

        self.model_name = self.request.GET.get("model_name", "").lower()
        if not self.model_name:
            raise AttributeError("model_name is required")

        self.object_name = self.request.GET.get("object_name", "").lower()
        if not self.object_name:
            raise AttributeError("object_name is required")

        self.field_name = self.request.GET.get("field_name", "")
        if not self.field_name:
            raise AttributeError("field_name is required")

        self.label_field_name = self.request.GET.get("label_field_name", "pk")
        self.view_perm = f"{self.app_label}.view_{self.object_name}"
        self.term = self.request.GET.get("term", "")


@dataclass
class ActivityRequestParser:
    request: InitVar[HttpRequest]
    app_label: str = field(init=False)
    model: str = field(init=False)

    def __post_init__(self, request: HttpRequest):
        self.app_label = request.GET.get("app_label")
        if self.app_label is None:
            raise Http404("app_label is required")

        self.model = request.GET.get("model")
        if self.model is None:
            raise Http404("model is required")

    def asdict(self) -> dict[str, str]:
        return asdict(self)


@dataclass
class ReportSchema:
    title: str
    report: list[dict[str, Any]] | dict = field(default=...)
    headers: list[str] = field(default_factory=list)

    def asdict(self) -> dict:
        return {
            "title": self.title,
            "headers": self.headers,
            "report": self.report,
        }

    def get_response(self, status_code: int = 200) -> Response:
        return Response(self.asdict(), status=status_code)

    def __post_init__(self):
        if not self.headers:
            if isinstance(self.report, dict):
                self.headers = list(self.report.keys())
            elif isinstance(self.report, list):
                if len(self.report) > 0:
                    self.headers = list(self.report[0].keys())
                else:
                    self.headers = []
            else:
                raise NotImplementedError(
                    "data must be an instance of list or dict",
                )
