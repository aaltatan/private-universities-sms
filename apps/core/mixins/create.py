import json
from abc import ABC, abstractmethod
from typing import Any

from django.contrib import messages
from django.db.models import Model
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext as _

from ..schemas import RequestParser


class CreateMixin(ABC):
    """
    A mixin that adds a create form.
    """

    @property
    @abstractmethod
    def form_class(self) -> type[ModelForm]:
        pass

    model: type[Model] | None = None
    template_name: str | None = None
    form_modal_template_name: str | None = None
    form_template_name: str | None = None

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Handles GET requests and returns a rendered template.
        """
        if self.can_access(request=request) is False:
            message = self.cannot_access_message(request=request)
            messages.error(request, message)

            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        request_parser = RequestParser(
            request=request,
            action="create",
            index_url=self.get_app_urls()["index_url"],
        )
        template_name = self.get_template_name()
        context = self.get_context_data()

        if request.htmx:
            if request_parser.is_modal_request:
                context["request_parser"] = request_parser.asdict()
                template_name = self.get_form_modal_template_name()
            else:
                template_name = self.get_form_template_name()

        return render(request, template_name, context)

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Handles the POST request.
        """
        form = self.form_class(request.POST, request.FILES)
        request_parser = RequestParser(
            request=request,
            action="create",
            index_url=self.get_app_urls()["index_url"],
        )

        if form.is_valid():
            return self.get_form_valid_response(
                request=request,
                form=form,
                request_parser=request_parser,
            )

        return self.get_form_invalid_response(
            request=request,
            form=form,
            request_parser=request_parser,
        )

    def can_access(self, request: HttpRequest) -> bool:
        """
        Hook for checking if the user has access to the view.
        """
        return True

    def cannot_access_message(self, request: HttpRequest) -> str:
        """
        Hook for returning the message to be displayed when the user does not have access to the view.
        """
        return _("you cannot access this page")

    def get_form_invalid_response(
        self,
        request: HttpRequest,
        form: type[ModelForm],
        request_parser: RequestParser,
    ) -> HttpResponse:
        """
        Returns the form invalid response.
        """
        context = self.get_context_data()
        context["form"] = form

        template_name = self.get_form_template_name()

        if request_parser.is_modal_request:
            template_name = self.get_form_modal_template_name()
            context["create_url"] = request.path
            response = render(request, template_name, context)
            response["Hx-Retarget"] = "#modal-container"
        else:
            response = render(request, template_name, context)

        messages.error(request, _("form is invalid"))
        response["Hx-Trigger"] = "messages"

        return response

    def perform_create(self, form: ModelForm) -> None:
        """
        Performs the create action, you can add custom logic here.
        """
        return form.save()

    def get_form_valid_response(
        self,
        request: HttpRequest,
        form: type[ModelForm],
        request_parser: RequestParser,
    ) -> HttpResponse:
        """
        Returns the form valid response.
        """
        obj = self.perform_create(form)
        messages.success(
            request,
            _("{} has been created successfully").format(obj),
        )

        response = HttpResponse(status=201)

        if request_parser.target == "#no-content":
            response["Hx-Reswap"] = "innerHTML"

        if request_parser.save:
            if not request_parser.dont_redirect:
                if request_parser.is_modal_request:
                    response["Hx-Location"] = request_parser.hx_location
                else:
                    response["Hx-Redirect"] = request_parser.index_url
        elif request_parser.save_and_add_another:
            context = self.get_context_data()
            response = render(
                request=request,
                template_name=self.get_form_template_name(),
                context=context,
                status=201,
            )
        elif request_parser.save_and_continue_editing:
            response["Hx-Redirect"] = obj.get_update_url() + request_parser.querystring

        response["Hx-Trigger"] = "messages"

        if request_parser.is_modal_request:
            response["Hx-Trigger"] = json.dumps(
                {
                    "hidemodal": "hiding modal after success request",
                    "messages": "getting messages",
                },
            )

        return response

    def get_model_class(self) -> type[Model]:
        """
        Returns the model class.
        """
        if self.model:
            return self.model

        return self.form_class.Meta.model

    def get_template_name(self) -> str:
        """
        Returns the template name.
        Notes: you can use the *template_name* attribute to override the default template name.
        """
        if self.template_name:
            return self.template_name

        codename_plural = self.get_codename_plural()
        app_label = self.get_app_label()

        return f"apps/{app_label}/{codename_plural}/create.html"

    def get_form_modal_template_name(self) -> str:
        """
        Returns the form modal template name.
        Notes: you can use the *form_modal_template_name* attribute to override the default form modal template name.
        """

        if self.form_template_name:
            return self.form_modal_template_name

        codename_plural = self.get_codename_plural()
        app_label = self.get_app_label()

        return f"components/{app_label}/{codename_plural}/modal-create.html"

    def get_form_template_name(self) -> str:
        """
        Returns the form template name.
        Notes: you can use the *form_template_name* attribute to override the default form template name.
        """
        if self.form_modal_template_name:
            return self.form_template_name

        app_label = self.get_app_label()
        codename_plural = self.get_codename_plural()

        return f"components/{app_label}/{codename_plural}/create.html"

    def get_codename_plural(self) -> str:
        """
        Returns the codename plural using the model.
        """
        return self.get_model_class()._meta.codename_plural

    def get_app_label(self) -> str:
        """
        Returns the app label using the model.
        """
        model = self.get_model_class()
        return model._meta.app_label

    def get_app_urls(self) -> dict[str, str]:
        """
        Returns the app links.
        """
        app_label = self.get_app_label()
        codename_plural = self.get_codename_plural()
        return {
            "index_url": reverse(f"{app_label}:{codename_plural}:index"),
            "create_url": reverse(f"{app_label}:{codename_plural}:create"),
        }

    def get_html_ids(self) -> dict[str, str]:
        """
        Returns the html ids.
        """
        codename_plural = self.get_codename_plural()
        return {
            "table_id": f"{codename_plural}-table",
            "form_id": f"{codename_plural}-form",
        }

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """
        Returns the context data that will be passed to the template.
        """
        context = {
            "form": self.form_class(),
            **self.get_app_urls(),
            **self.get_html_ids(),
        }
        return context
