import json
from abc import ABC, abstractmethod
from typing import Any

from django.contrib import messages
from django.db.models import Model
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ..forms import BehaviorForm
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
    form_class: type[BehaviorForm] | None = None

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

        self.obj = get_object_or_404(self.get_model_class(), slug=slug)

        if not self.can_access(request, self.obj):
            messages.error(
                request,
                self.cannot_access_message(request, self.obj),
            )
            raise Http404()

        modal_template_name = self.get_modal_template_name()

        if self.form_class is not None:
            form = self.form_class()
            context = self.context_data(form=form)
        else:
            context = self.context_data()

        response = render(request, modal_template_name, context)
        response["HX-Trigger"] = "showmodal"
        return response

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

        if self.form_class is None:
            return self.get_behavior_response(request, behavior)
        else:
            form = self.form_class(request.POST)
            if form.is_valid():
                return self.get_behavior_response(request, behavior, form)
            else:
                return render(
                    request=request,
                    template_name=self.get_modal_template_name(),
                    context=self.context_data(form=form),
                )

    def get_success_response(self, request: HttpRequest, message: str):
        response = HttpResponse()
        querystring = request.GET.urlencode() and f"?{request.GET.urlencode()}"
        messages.success(request, message)
        response["Hx-Location"] = json.dumps(
            {
                "path": self.get_index_url() + querystring,
                "target": f"#{self.get_html_ids()['table_id']}",
            }
        )
        response["HX-Trigger"] = "messages, hidemodal"
        return response

    def get_error_response(self, request: HttpRequest, message: str):
        response = HttpResponse()

        response["Hx-Retarget"] = "#no-content"
        response["HX-Reswap"] = "innerHTML"
        messages.error(request, message)
        response["HX-Trigger"] = "messages, hidemodal"

        return response

    def get_behavior_response(
        self,
        request: HttpRequest,
        behavior: ActionBehavior,
        form: BehaviorForm | None = None,
    ):
        behavior.action()
        message = behavior.get_message()

        if behavior.has_executed:
            if form is not None:
                form.save()
            return self.get_success_response(request, message)
        else:
            return self.get_error_response(request, message)

    def can_access(self, request: HttpRequest, obj: Model) -> bool:
        """
        Hook for checking if the user has access to the view.
        """
        return True

    def cannot_access_message(self, request: HttpRequest, obj: Model) -> str:
        """
        Hook for returning the message to be displayed when the user does not have access to the view.
        """
        return _("you cannot access this page")

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

    def get_codename_plural(self) -> str:
        """
        Returns the codename plural using the model.
        """
        model = self.get_model_class()
        return model._meta.codename_plural

    def get_html_ids(self) -> dict[str, str]:
        """
        Returns the html ids.
        """
        return {
            "table_id": f"{self.get_codename_plural()}-table",
        }

    def get_index_url(self) -> str:
        """
        Returns the app links.
        """
        app_label = self.get_app_label()
        codename_plural = self.get_codename_plural()
        return reverse(f"{app_label}:{codename_plural}:index")

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
