import json

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db.models import QuerySet
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from ..models import Activity
from ..utils import Deleter


class CreateActivitiesMixin:
    def create_activities(self, qs: QuerySet) -> None:
        activities: list[Activity] = []

        content_type = ContentType.objects.get_for_model(
            self.get_model_class(),
        )

        for obj in qs:
            serializer: type[ModelSerializer] = self.activity_serializer(obj)
            activity = Activity(
                user=self.request.user,
                kind=Activity.KindChoices.DELETE,
                content_type=content_type,
                object_id=obj.pk,
                data=serializer.data,
            )
            activities.append(activity)
        
        return activities


class BulkDeleteMixin(CreateActivitiesMixin):
    def bulk_delete(self, qs: QuerySet, **kwargs) -> HttpResponse:
        if getattr(self, "deleter", None) is None:
            raise AttributeError(
                "you must define a deleter class for the ListView.",
            )
        
        if type(self.deleter) == Deleter:
            raise TypeError(
                "the deleter class must be a subclass of Deleter.",
            )

        activities = self.create_activities(qs=qs)
        deleter: Deleter = self.deleter(queryset=qs)
        deleter.delete()

        if deleter.has_deleted:
            Activity.objects.bulk_create(activities)
            response = HttpResponse(status=204)
            response["Hx-Location"] = json.dumps(
                {
                    "path": self.request.get_full_path(),
                    "target": f"#{self.get_html_ids()['table_id']}",
                }
            )
            messages.success(
                self.request,
                deleter.get_message(),
            )
            response["HX-Trigger"] = "messages"
            return response
        else:
            response = HttpResponse()
            response["Hx-Retarget"] = "#no-content"
            response["HX-Reswap"] = "innerHTML"
            response["HX-Trigger"] = "messages"
            messages.error(
                self.request,
                deleter.get_message(),
            )
            return response


class BulkDeleteAPIMixin(CreateActivitiesMixin):
    @action(detail=False, methods=["post"], url_path="bulk-delete")
    def bulk_delete(self, request: Request):
        """
        Deletes the selected objects.
        """
        if getattr(self, "deleter", None) is None:
            raise AttributeError(
                "you must define a deleter class for the ListView.",
            )

        if type(self.deleter) == Deleter:
            raise TypeError(
                "the deleter class must be a subclass of Deleter.",
            )

        ids = request.data.get("ids", [])
        qs: QuerySet = self.queryset.filter(pk__in=ids)
        activities = self.create_activities(qs=qs)

        if not qs.exists():
            return Response(
                {"details": _("no objects found")},
                status=status.HTTP_404_NOT_FOUND,
            )

        deleter: Deleter = self.deleter(queryset=qs)
        deleter.delete()

        if deleter.has_deleted:
            Activity.objects.bulk_create(activities)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"details": deleter.get_message()},
                status=status.HTTP_400_BAD_REQUEST,
            )
