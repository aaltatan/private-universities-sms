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
    Model = instance.__class__

    slug_exists = Model.objects.filter(slug=slug).exclude(pk=instance.pk).exists()

    if slug_exists:
        slug = utils.increase_slug_by_one(slug)
        return slugify_name(
            sender=sender,
            instance=instance,
            slug=slug,
        )

    instance.slug = slug
