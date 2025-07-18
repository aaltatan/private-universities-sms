from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from ..utils import ActionBehavior


class BulkDeleteAPIMixin:
    @action(detail=False, methods=["post"], url_path="bulk-delete")
    def bulk_delete(self, request: Request):
        """
        Deletes the selected objects.
        """
        if getattr(self, "deleter", None) is None:
            raise AttributeError(
                "you must define a deleter class for the ListView.",
            )

        if not issubclass(self.deleter, ActionBehavior):
            raise TypeError(
                "the deleter class must be a subclass of ActionBehavior.",
            )

        ids = request.data.get("ids", [])
        qs: QuerySet = self.queryset.filter(pk__in=ids)

        if not qs.exists():
            return Response(
                {"details": _("no objects found")},
                status=status.HTTP_404_NOT_FOUND,
            )

        deleter: ActionBehavior = self.deleter(
            request=self.request,
            queryset=qs,
        )
        deleter.action()

        if deleter.has_executed:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"details": deleter.get_message()},
                status=status.HTTP_400_BAD_REQUEST,
            )
