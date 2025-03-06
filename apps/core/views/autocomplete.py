from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldError
from django.db.models import Model
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from ..schemas import AutocompleteRequestParser
from ..utils import get_djangoql_query, get_keywords_query


class AutocompleteView(View):
    """
    A view that handles autocomplete requests.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        try:
            parser = AutocompleteRequestParser(request=request)
        except AttributeError as e:
            return HttpResponse(str(e), status=400)

        Model = self.get_model_class(parser=parser)

        try:
            default_queryset = Model.objects.filter(
                get_keywords_query(
                    parser.term,
                    field_name=parser.field_name,
                ),
            )
        except FieldError as e:
            return HttpResponse(str(e), status=400)

        qs = get_djangoql_query(
            qs_to_filter=Model.objects.all(),
            djangoql_query=parser.term,
            default_queryset=default_queryset,
        )

        context = {
            "object_list": qs,
            "label_field_name": parser.label_field_name,
        }

        return render(request, "widgets/autocomplete-item.html", context)

    def post(self, request: HttpRequest, pk: str, *args, **kwargs) -> HttpResponse:
        try:
            parser = AutocompleteRequestParser(request=request)
        except AttributeError as e:
            return HttpResponse(str(e), status=400)

        Model = self.get_model_class(parser=parser)

        instance = get_object_or_404(Model, pk=pk)

        return JsonResponse(
            {
                "value": getattr(instance, parser.label_field_name, None),
            }
        )

    def get_model_class(self, parser: AutocompleteRequestParser) -> type[Model] | None:
        content_type = get_object_or_404(
            ContentType, app_label=parser.app_label, model=parser.model_name
        )
        return content_type.model_class()
