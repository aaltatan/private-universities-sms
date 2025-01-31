import json
from abc import ABC, abstractmethod
from typing import Any

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import gettext as _
from rest_framework.serializers import ModelSerializer

from ..models import Activity
from ..utils import BaseDeleter


class DeleteMixin(ABC):
    @property
    @abstractmethod
    def activity_serializer(self) -> type[ModelSerializer]:
        pass

    def __init__(self):
        if getattr(self, "deleter", None) is None:
            raise AttributeError(
                "you must define a deleter class for the ListView.",
            )

        if not issubclass(self.deleter, BaseDeleter):
            raise TypeError(
                "the deleter class must be a subclass of Deleter.",
            )

    def get(self, request: HttpRequest, slug: str, *args, **kwargs) -> HttpResponse:
        """
        Handles GET requests and returns a rendered template.
        """
        if not request.htmx:
            messages.error(
                request,
                _("you can't delete this object because you are not using htmx."),
            )
            raise Http404()

        model = self.get_model_class()
        self.obj = get_object_or_404(model, slug=slug)
        modal_template_name = self.get_modal_template_name()
        context = self.context_data()

        return render(request, modal_template_name, context)

    def post(self, request: HttpRequest, slug: str, *args, **kwargs) -> HttpResponse:
        """
        Handles the POST request.
        """
        if not request.htmx:
            messages.error(
                request,
                _("you can't delete this object because you are not using htmx."),
            )
            raise Http404()

        model = self.get_model_class()
        self.obj = get_object_or_404(model, slug=slug)

        deleter: type[BaseDeleter] = self.deleter(self.obj)

        if deleter.is_deletable():
            serializer = self.activity_serializer(self.obj)
            Activity.objects.create(
                user=request.user,
                kind=Activity.KindChoices.DELETE,
                content_type=ContentType.objects.get_for_model(self.obj),
                object_id=self.obj.pk,
                data=serializer.data,
            )
            deleter.delete()
            response = HttpResponse(status=204)
            querystring = request.GET.urlencode() and f"?{request.GET.urlencode()}"
            messages.success(request, deleter.get_message(self.obj))
            response["Hx-Location"] = json.dumps(
                {
                    "path": self.get_app_urls()["index_url"] + querystring,
                    "target": f"#{self.get_html_ids()['table_id']}",
                }
            )
        else:
            response = HttpResponse(status=200)
            response["Hx-Retarget"] = "#no-content"
            response["HX-Reswap"] = "innerHTML"
            messages.error(request, deleter.get_message(self.obj))

        response["HX-Trigger"] = "messages"

        return response

    def context_data(self, **kwargs) -> dict[str, Any]:
        """
        Returns the context data that will be passed to the template.
        """
        return {
            "obj": self.obj,
            **self.get_html_ids(),
            **kwargs,
        }

    def get_app_label(self) -> str:
        """
        Returns the app label using the model.
        """
        model = self.get_model_class()
        return model._meta.app_label

    def get_html_ids(self) -> dict[str, str]:
        """
        Returns the html ids.
        """
        return {
            "table_id": f"{self.get_app_label()}-table",
        }

    def get_app_urls(self) -> dict[str, str]:
        """
        Returns the app links.
        """
        app_label = self.get_app_label()
        return {
            "index_url": reverse(f"{app_label}:index"),
        }

    def get_modal_template_name(self) -> str:
        """
        Returns the modal template name.
        Notes: you can use the *modal_template_name* attribute to override the default modal template name.
        """
        if getattr(self, "modal_template_name", None):
            return self.modal_template_name
        return "components/blocks/modals/delete.html"

    def get_model_class(self) -> type[Model]:
        """
        Returns the model class.
        """
        if getattr(self, "model", None) is not None:
            return self.model
        
        return self.activity_serializer.Meta.model
