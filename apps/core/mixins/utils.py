from dataclasses import dataclass, field, InitVar


@dataclass
class ModalParser:
    """A dataclass that represents a modal headers."""

    headers: InitVar[dict]
    is_modal_request: bool = field(default=False, init=False)
    querystring: str = field(init=False)
    redirect_to: str = field(init=False)
    redirect: bool = field(default=False, init=False)
    url: str = field(init=False, default="")

    def __post_init__(self, headers: dict):
        self.is_modal_request = headers.get("modal") is not None
        self.querystring = headers.get("querystring", "")
        self.redirect_to = headers.get("redirect-to", "")

        if self.redirect_to:
            self.redirect = True

        if self.is_modal_request:
            self.url = self.redirect_to + self.querystring
