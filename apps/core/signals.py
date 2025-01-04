from typing import Any

from django.utils.text import slugify

from . import models


def slugify_name(
    sender: Any,
    instance: type[models.AbstractUniqueNameModel],
    *args,
    **kwargs: dict[str, Any],
) -> None:
    instance.slug = slugify(instance.name, allow_unicode=True)
