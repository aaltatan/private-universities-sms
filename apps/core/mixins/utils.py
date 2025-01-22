from dataclasses import InitVar, asdict, dataclass, field
from typing import Any

from django.http import HttpRequest


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
