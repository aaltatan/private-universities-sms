from django.contrib.contenttypes.models import ContentType
from django.http import (
    Http404,
    HttpRequest,
    HttpResponse,
    HttpResponseForbidden,
)
from django.shortcuts import render

from ..models import Activity
from ..schemas import ActivityRequestParser


def activities(
    request: HttpRequest,
    object_id: int,
    *args,
    **kwargs,
) -> HttpResponse:
    parser = ActivityRequestParser(request=request)
    content_type = ContentType.objects.filter(**parser.asdict()).first()

    if not content_type:
        raise Http404()

    Model = content_type.model_class()

    app_label = Model._meta.app_label
    object_name = Model._meta.object_name.lower()

    required_permission = f"{app_label}.view_activity_{object_name}"

    if not request.user.has_perm(required_permission):
        return HttpResponseForbidden(
            "You don't have permission to perform this action",
        )

    if content_type is None:
        raise Http404()

    qs = Activity.objects.filter(
        content_type=content_type,
        object_id=object_id,
    )

    context = {"activities": qs}

    return render(request, "apps/core/activities.html", context)
