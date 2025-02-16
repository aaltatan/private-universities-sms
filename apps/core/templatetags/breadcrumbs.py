from dataclasses import dataclass, field, InitVar, asdict
from itertools import accumulate

from django import template
from django.http import HttpRequest
from django.urls import Resolver404, resolve, ResolverMatch


@dataclass
class Path:
    resolver: InitVar[ResolverMatch]
    path: str = field(init=False, default="")
    title: str = field(init=False, default="")

    def __post_init__(self, resolver: ResolverMatch):
        self.path = resolver.route
        title = resolver.kwargs.get("title")

        if title is None:
            raise ValueError(
                f"title is required in <{resolver.app_name}:{resolver.view_name}>",
            )

        self.title = title

        if "slug" in resolver.route:
            slug: str = resolver.kwargs.get("slug", "")
            self.title += " " + slug.replace("-", " ").title()

        self.path = f"/{self.path}"

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
