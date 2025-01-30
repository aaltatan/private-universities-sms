from dataclasses import InitVar, asdict, dataclass, field
from typing import Any, Callable, Literal, Sequence

from django.db.models import QuerySet, Q
from django.http import Http404, HttpRequest, HttpResponse

from .constants import PERMISSION


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
class RequestParser:
    """A dataclass that represents the required data from http request."""

    request: InitVar[HttpRequest]
    index_url: str
    is_modal_request: bool = field(init=False)
    next_url: str = field(init=False, default="")
    target: str = field(init=False, default="")
    dont_redirect: bool = field(init=False)

    def __post_init__(self, request: HttpRequest):
        self.is_modal_request = request.headers.get("modal") is not None

        self.target = request.headers.get("target")
        if not self.target and self.is_modal_request:
            raise ValueError("target is required")

        self.dont_redirect = request.headers.get("dont-redirect") is not None

        querystring = request.GET.urlencode()
        querystring = querystring and f"?{querystring}"
        self.index_url += querystring

        self.next_url = request.headers.get("referer", self.index_url)

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

    def __post_init__(self):
        self.app_label = self.request.GET.get("app_label", "")
        if not self.app_label:
            raise Http404("app_label is required")

        self.model_name = self.request.GET.get("model_name", "").lower()
        if not self.model_name:
            raise Http404("model_name is required")

        self.object_name = self.request.GET.get("object_name", "").lower()
        if not self.object_name:
            raise Http404("object_name is required")

        self.field_name = self.request.GET.get("field_name", "")
        if not self.field_name:
            raise Http404("field_name is required")

        self.label_field_name = self.request.GET.get("label_field_name", "pk")

        self.term = self.request.GET.get("term", "")

    def get_term_query(
        self,
        join: Literal["and", "or"] = "and",
        type: Literal["word", "letter"] = "word",
    ) -> Q:
        """
        Returns a search query.
        """
        query: Q = Q()
        keywords: Sequence[str] = ""

        if type == "word":
            keywords = self.term.split(" ")
        elif type == "letter":
            keywords = self.term

        for word in keywords:
            if join == "and":
                query &= Q(search__icontains=word)
            else:
                query |= Q(search__icontains=word)

        return query
