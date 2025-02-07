from dataclasses import dataclass, field, InitVar, asdict
from itertools import accumulate

from django import template
from django.http import HttpRequest
from django.urls import Resolver404, resolve, ResolverMatch


@dataclass
class Path:
    path: InitVar[ResolverMatch]
    href: str = field(init=False, default="")
    text: str = field(init=False, default="")

    def __post_init__(self, path: ResolverMatch):
        self.href = path.route
        self.text = path.kwargs.get("title")

        if path.url_name == "update":
            slug: str = path.kwargs.get("slug", "")
            self.href = path.route.replace("<str:slug>", slug)

            self.text = slug.replace("-", " ").title()

        self.href = f"/{self.href}"

    def model_dump(self) -> dict[str, str]:
        return asdict(self)


register = template.Library()


@register.simple_tag(takes_context=True)
def get_breadcrumbs(context):
    request: HttpRequest | None = context.get("request")
    path_keywords = [p for p in request.path.split("/") if p]
    paths = list(
        accumulate(path_keywords, lambda a, b: f"{a}/{b}"),
    )

    breadcrumbs: list[Path] = []

    for path in paths:
        path = f"/{path}/"
        try:
            path = resolve(path)
            breadcrumbs.append(Path(path).model_dump())
        except Resolver404:
            pass
    
    return breadcrumbs
