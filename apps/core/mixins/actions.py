import json

from django.db.models import QuerySet
from django.http import HttpResponse

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from ..utils import Deleter


class BulkDeleteMixinBase:
    def raise_errors(self, message: str) -> HttpResponse:
        if getattr(self, "deleter", None) is None:
            raise AttributeError(
                "you must define a deleter class for the ListView.",
            )

        if not issubclass(self.deleter, Deleter):
            raise TypeError(
                "the deleter class must be a subclass of Deleter.",
            )

class BulkDeleteMixin:
    def bulk_delete(self, qs: QuerySet, **kwargs) -> HttpResponse:
        if getattr(self, "deleter", None) is None:
            raise AttributeError(
                "you must define a deleter class for the ListView.",
            )

        if not issubclass(self.deleter, Deleter):
            raise TypeError(
                "the deleter class must be a subclass of Deleter.",
            )

        deleter = self.deleter(qs, self.request)

        is_deletable = deleter.delete()

        if is_deletable:
            response = HttpResponse(status=204)
            response["Hx-Location"] = json.dumps(
                {
                    "path": self.request.get_full_path(),
                    "target": f"#{self.get_html_ids()['table_id']}",
                }
            )
            response["HX-Trigger"] = "messages"
            return response
        else:
            response = HttpResponse()
            response["Hx-Retarget"] = "#no-content"
            response["HX-Reswap"] = "innerHTML"
            response["HX-Trigger"] = "messages"
            return response


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

        if not issubclass(self.deleter, Deleter):
            raise TypeError(
                "the deleter class must be a subclass of Deleter.",
            )

        ids = request.data.get("ids", [])
        qs = self.queryset.filter(pk__in=ids)

        deleter = self.deleter(
            qs,
            send_error_messages=False,
            send_success_messages=False,
        )
        is_deletable = deleter.delete()

        if is_deletable:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {
                    "details": deleter.get_qs_error_message(qs),
                    "status": status.HTTP_400_BAD_REQUEST,
                }
            )
