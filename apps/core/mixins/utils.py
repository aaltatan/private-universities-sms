from dataclasses import dataclass, field, InitVar

from django.http import HttpRequest


@dataclass
class RequestParser:
    """A dataclass that represents the required data from http request."""

    request: InitVar[HttpRequest]
    is_modal_request: bool = field(default=False, init=False)
    querystring: str = field(init=False)
    redirect_to: str = field(init=False)
    redirect: bool = field(default=False, init=False)
    url: str = field(init=False, default="")

    def __post_init__(self, request: HttpRequest):
        self.is_modal_request = request.headers.get("modal") is not None
        self.querystring = request.headers.get("querystring", "")
        self.redirect_to = request.headers.get("redirect-to", "")

        if self.redirect_to:
            self.redirect = True

        if self.is_modal_request:
            self.url = self.redirect_to + self.querystring
