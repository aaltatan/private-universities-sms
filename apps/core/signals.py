from typing import Any

from django.utils.text import slugify

from . import models, utils


def slugify_name(
    sender: Any,
    instance: type[models.AbstractUniqueNameModel],
    *args,
    **kwargs: dict[str, Any],
) -> None:
    slug = kwargs.get(
        "slug",
        slugify(instance.name, allow_unicode=True),
    )
    class_ = instance.__class__

    slug_exists = class_.objects.filter(slug=slug).exists()

    if slug_exists:
        slug = utils.increase_slug_by_one(slug)
        return slugify_name(
            sender=sender,
            instance=instance,
            slug=slug,
        )
    
    instance.slug = slug
