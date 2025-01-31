from abc import ABC, abstractmethod

from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from ..models import Activity
from ..utils import BaseDeleter, get_differences


class APIMixin(ABC):
    @property
    @abstractmethod
    def activity_serializer(self) -> type[ModelSerializer]:
        pass

    @property
    @abstractmethod
    def deleter(self) -> type[BaseDeleter]:
        pass

    def destroy(self, request, *args, **kwargs):
        if getattr(self, "deleter", None) is None:
            raise AttributeError(
                "you must define a deleter class for the ListView.",
            )

        if not issubclass(self.deleter, BaseDeleter):
            raise TypeError(
                "the deleter class must be a subclass of Deleter.",
            )

        instance = self.get_object()

        deleter: type[BaseDeleter] = self.deleter(instance)

        if deleter.is_deletable():
            serializer = self.serializer_class(instance)
            Activity.objects.create(
                user=request.user,
                kind=Activity.KindChoices.DELETE,
                content_type=ContentType.objects.get_for_model(instance),
                object_id=instance.pk,
                data=serializer.data,
            )
            deleter.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"details": deleter.get_message(instance)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def perform_update(self, serializer):
        from_data = self.activity_serializer(serializer.instance).data
        instance_after_update = serializer.save()
        to_data = self.activity_serializer(instance_after_update).data

        differences = get_differences(from_data, to_data)

        Activity.objects.create(
            user=self.request.user,
            kind=Activity.KindChoices.UPDATE,
            content_type=ContentType.objects.get_for_model(
                instance_after_update,
            ),
            object_id=instance_after_update.pk,
            data=differences,
        )

    def perform_create(self, serializer):
        instance = serializer.save()
        Activity.objects.create(
            user=self.request.user,
            kind=Activity.KindChoices.CREATE,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.pk,
        )

    def get_model_class(self):
        queryset = self.get_queryset()
        return queryset.model
