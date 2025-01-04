import json

from django.db.models import QuerySet
from django.http import HttpResponse, HttpRequest

from ..utils import Deleter


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
        
        request: HttpRequest = self.request

        is_deletable = self.deleter(qs, request).delete()

        if is_deletable:
            response = HttpResponse(status=204)
            response["Hx-Location"] = json.dumps(
                {
                    "path": request.get_full_path(),
                    "target": f"#{self.get_html_ids()['table_id']}",
                }
            )
        else:
            response = HttpResponse()
            response["Hx-Retarget"] = "#no-content"
            response["HX-Reswap"] = "innerHTML"

        response["HX-Trigger"] = "messages"

        return response
