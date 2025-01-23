from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render

from .schemas import AutocompleteRequestParser


@login_required
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "apps/core/index.html")


@login_required
def messages(request: HttpRequest) -> HttpResponse:
    return render(request, "apps/core/messages.html")


@login_required
def autocomplete(request: HttpRequest) -> HttpResponse:
    parser = AutocompleteRequestParser(request=request)
    content_type = get_object_or_404(
        ContentType,
        app_label=parser.app_label,
        model=parser.model_name,
    )

    view_perm = get_object_or_404(
        Permission,
        codename=f"view_{parser.object_name}",
    )
    if not request.user.has_perm(view_perm) and not request.user.is_superuser:
        return HttpResponseForbidden()

    Model = content_type.model_class()

    if getattr(Model, parser.field_name, None) is None:
        return HttpResponse(
            f"field {parser.field_name} does not exist",
            status=400,
        )

    qs = Model.objects.filter(
        **{f"{parser.field_name}__icontains": parser.term},
    )
    context = {"object_list": qs}

    return render(request, "apps/core/autocomplete-item.html", context)
