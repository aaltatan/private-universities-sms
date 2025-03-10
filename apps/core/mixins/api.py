from abc import ABC, abstractmethod

from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.response import Response

from ..models import Activity
from ..utils import Deleter


class APIMixin(ABC):
    @property
    @abstractmethod
    def deleter(self) -> Deleter:
        pass

    def destroy(self, request, *args, **kwargs):
        if getattr(self, "deleter", None) is None:
            raise AttributeError(
                "you must define a deleter class for the ListView.",
            )
        if not issubclass(self.deleter, Deleter):
            raise TypeError(
                "the deleter class must be a subclass of Deleter.",
            )

        instance = self.get_object()

        deleter: Deleter = self.deleter(obj=instance)
        deleter.delete()

        if deleter.has_deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"details": deleter.get_message()},
                status=status.HTTP_400_BAD_REQUEST,
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
