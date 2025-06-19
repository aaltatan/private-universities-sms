from abc import ABC, abstractmethod

from rest_framework import status
from rest_framework.response import Response

from ..utils import ActionBehavior


class APIMixin(ABC):
    @property
    @abstractmethod
    def behavior(self) -> ActionBehavior:
        pass

    def destroy(self, request, *args, **kwargs):
        if getattr(self, "behavior", None) is None:
            raise AttributeError(
                "you must define a behavior class for the ListView.",
            )
        if not issubclass(self.behavior, ActionBehavior):
            raise TypeError(
                "the behavior class must be a subclass of ActionBehavior.",
            )

        instance = self.get_object()

        deleter: ActionBehavior = self.behavior(
            request=self.request,
            obj=instance,
        )
        deleter.action()

        if deleter.has_executed:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"details": deleter.get_message()},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get_model_class(self):
        queryset = self.get_queryset()
        return queryset.model
