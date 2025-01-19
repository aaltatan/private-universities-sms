from rest_framework import status
from rest_framework.response import Response

from apps.core.utils import Deleter


class DestroyMixin:
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

        deleter: type[Deleter] = self.deleter(instance)

        if deleter.is_deletable():
            deleter.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"details": deleter.get_message(instance)},
                status=status.HTTP_400_BAD_REQUEST,
            )
