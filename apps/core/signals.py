from typing import Any, Callable

from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from rest_framework import serializers

from . import models, utils
from .middlewares import RequestMiddleware


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


def add_update_activity(
    activity_serializer: serializers.ModelSerializer,
) -> Callable[..., None]:
    def _add_update_activity(
        sender: Any, instance: models.Activity, *args, **kwargs: dict[str, Any]
    ) -> None:
        request = RequestMiddleware.get_current_request()

        if request and instance.pk is not None:
            Model = instance.__class__
            old_instance = Model.objects.get(pk=instance.pk)

            old_instance_data = activity_serializer(old_instance).data
            instance_data = activity_serializer(instance).data

            differences = utils.get_differences(old_instance_data, instance_data)

            if differences:
                models.Activity.objects.create(
                    user=request.user,
                    kind=models.Activity.KindChoices.UPDATE,
                    content_type=ContentType.objects.get_for_model(instance),
                    object_id=instance.pk,
                    data=differences,
                )

    return _add_update_activity


def add_delete_activity(
    activity_serializer: serializers.ModelSerializer,
) -> Callable[..., None]:
    def _add_delete_activity(
        sender: Any, instance: models.Activity, *args, **kwargs: dict[str, Any]
    ) -> None:
        request = RequestMiddleware.get_current_request()

        if request and instance.pk is not None:
            instance_data = activity_serializer(instance).data

            models.Activity.objects.create(
                user=request.user,
                kind=models.Activity.KindChoices.DELETE,
                content_type=ContentType.objects.get_for_model(instance),
                object_id=instance.pk,
                data=instance_data,
            )

    return _add_delete_activity
