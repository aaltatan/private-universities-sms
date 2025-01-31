from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from ..models import Activity
from ..schemas import ActivityRequestParser
from ..auth import superuser_required


@superuser_required
def activities(request: HttpRequest, object_id: int, *args, **kwargs) -> HttpResponse:
    parser = ActivityRequestParser(request=request)
    content_type = ContentType.objects.filter(**parser.asdict()).first()

    if content_type is None:
        raise Http404()

    qs = Activity.objects.filter(
        content_type=content_type,
        object_id=object_id,
    )

    context = {"activities": qs}

    return render(request, "apps/core/activities.html", context)
