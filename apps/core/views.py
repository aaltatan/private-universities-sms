from django.contrib.auth.decorators import login_required
from django.views import View
from django.db.models import Model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render

from .schemas import AutocompleteRequestParser


@login_required
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "apps/core/index.html")


@login_required
def messages(request: HttpRequest) -> HttpResponse:
    return render(request, "apps/core/messages.html")


class AutocompleteView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        parser = AutocompleteRequestParser(request=request)
        self.check_permissions(request=request, parser=parser)

        Model = self.get_model_class(parser=parser)

        # if getattr(Model, parser.field_name, None) is None:
        #     return HttpResponse(
        #         f"field {parser.field_name} does not exist",
        #         status=400,
        #     )

        qs = Model.objects.filter(parser.get_term_query())
        context = {
            "object_list": qs,
            "label_field_name": parser.label_field_name,
        }

        return render(request, "widgets/autocomplete-item.html", context)

    def check_permissions(
        self,
        request: HttpRequest,
        parser: AutocompleteRequestParser,
    ) -> HttpResponseForbidden | None:
        view_perm = get_object_or_404(
            Permission,
            codename=f"view_{parser.object_name}",
        )
        if not request.user.has_perm(view_perm) and not request.user.is_superuser:
            return HttpResponseForbidden()
        return

    def get_model_class(self, parser: AutocompleteRequestParser) -> type[Model] | None:
        content_type = get_object_or_404(
            ContentType,
            app_label=parser.app_label,
            model=parser.model_name,
        )
        return content_type.model_class()

    def post(
        self,
        request: HttpRequest,
        pk: str,
        *args,
        **kwargs,
    ) -> HttpResponse:
        parser = AutocompleteRequestParser(request=request)
        self.check_permissions(request=request, parser=parser)

        Model = self.get_model_class(parser=parser)

        instance = get_object_or_404(Model, pk=pk)

        return JsonResponse(
            {
                "value": getattr(instance, parser.label_field_name, None),
            }
        )
