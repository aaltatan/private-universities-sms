import json
from abc import ABC, abstractmethod
from typing import Any

from django.contrib import messages
from django.db.models import Model
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import gettext as _

from ..utils import ActionBehavior


class BehaviorMixin(ABC):
    @property
    @abstractmethod
    def model(self) -> type[Model]:
        pass

    @property
    @abstractmethod
    def behavior(self) -> type[ActionBehavior]:
        pass

    modal_template_name: str | None = None

    def __init__(self):
        if getattr(self, "behavior", None) is None:
            raise AttributeError(
                "you must define a behavior class for the ListView.",
            )
        if not issubclass(self.behavior, ActionBehavior):
            raise TypeError(
                "the behavior class must be a subclass of ActionBehavior.",
            )

    def get(self, request: HttpRequest, slug: str, *args, **kwargs) -> HttpResponse:
        """
        Handles GET requests and returns a rendered template.
        """
        if not request.htmx:
            messages.error(
                request,
                _("you can't execute this action because you are not using htmx."),
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
                _("you can't execute this action because you are not using htmx."),
            )
            raise Http404()

        model = self.get_model_class()
        self.obj = get_object_or_404(model, slug=slug)

        behavior: ActionBehavior = self.behavior(request=self.request, obj=self.obj)

        behavior.action()

        if behavior.has_executed:
            response = HttpResponse(status=204)
            querystring = request.GET.urlencode() and f"?{request.GET.urlencode()}"
            messages.success(request, behavior.get_message())
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
            messages.error(request, behavior.get_message())

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

    def get_verbose_name_plural(self) -> str:
        """
        Returns the verbose name plural using the model.
        """
        model = self.get_model_class()
        return model._meta.codename_plural

    def get_html_ids(self) -> dict[str, str]:
        """
        Returns the html ids.
        """
        return {
            "table_id": f"{self.get_verbose_name_plural()}-table",
        }

    def get_app_urls(self) -> dict[str, str]:
        """
        Returns the app links.
        """
        app_label = self.get_app_label()
        verbose_name_plural = self.get_verbose_name_plural()
        return {
            "index_url": reverse(f"{app_label}:{verbose_name_plural}:index"),
        }

    def get_modal_template_name(self) -> str:
        """
        Returns the modal template name.
        Notes: you can use the *modal_template_name* attribute to override the default modal template name.
        """
        if self.modal_template_name:
            return self.modal_template_name
        return "components/blocks/modals/delete.html"

    def get_model_class(self) -> type[Model]:
        """
        Returns the model class.
        """
        return self.model
