import json
from typing import Any
from abc import ABC, abstractmethod

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext as _
from django.db.models import Model
from django.forms import ModelForm

from .utils import ModalParser


class AbstractUpdateMixin(ABC):
    @property
    @abstractmethod
    def form_class(self) -> type[ModelForm]: ...


class UpdateMixin(AbstractUpdateMixin):
    """
    A mixin that adds an update form.
    """

    def get(self, request: HttpRequest, slug: str, *args, **kwargs) -> HttpResponse:
        """
        Handles GET requests and returns a rendered template.
        """
        model = self.get_model_class()
        self.obj = get_object_or_404(model, slug=slug)
        headers_parser = ModalParser(request.headers)

        template_name = self.get_template_name()

        if request.htmx:
            if headers_parser.is_modal_request:
                template_name = self.get_form_modal_template_name()
            else:
                template_name = self.get_form_template_name()

        context = self.get_context_data()
        return render(request, template_name, context)

    def post(self, request: HttpRequest, slug: str, *args, **kwargs) -> HttpResponse:
        """
        Handles the POST request.
        """
        model = self.get_model_class()
        self.obj = get_object_or_404(model, slug=slug)

        form = self.form_class(request.POST, instance=self.obj)

        headers_parser = ModalParser(request.headers)

        if form.is_valid():
            return self.get_form_valid_response(
                request=request,
                form=form,
                headers_parser=headers_parser,
            )

        return self.get_form_invalid_response(
            request=request,
            form=form,
            headers_parser=headers_parser,
        )

    def get_form_valid_response(
        self,
        request: HttpRequest,
        form: type[ModelForm],
        headers_parser: ModalParser,
    ) -> HttpResponse:
        """
        Returns the form valid response.
        """
        app_label = self.get_app_label()
        obj = form.save()
        querystring = request.GET.urlencode() and f"?{request.GET.urlencode()}"

        messages.success(
            request,
            _("({}) has been updated successfully").format(obj),
        )

        url = reverse(f"{app_label}:index")

        response = HttpResponse(status=200)

        if not headers_parser.is_modal_request:
            response["Hx-Redirect"] = url + querystring
        if headers_parser.redirect:
            target = f'#{self.get_html_ids()["table_id"]}'
            response["Hx-Location"] = json.dumps(
                {
                    "path": headers_parser.url,
                    "target": target,
                },
            )

        response["Hx-Trigger"] = "messages"

        return response

    def get_form_invalid_response(
        self,
        request: HttpRequest,
        form: type[ModelForm],
        headers_parser: ModalParser,
    ) -> HttpResponse:
        """
        Returns the form invalid response.
        """
        template_name = self.get_form_template_name()
        context = self.get_context_data()
        context["form"] = form

        if headers_parser.is_modal_request:
            template_name = self.get_form_modal_template_name()
            context["create_url"] = request.path
            response = render(request, template_name, context)
            response["Hx-Retarget"] = "#modal-container"
        else:
            response = render(request, template_name, context)
        return response

    def get_model_class(self) -> type[Model]:
        """
        Returns the model class.
        """
        if getattr(self, "model", None):
            return self.model

        return self.form_class.Meta.model

    def get_template_name(self) -> str:
        """
        Returns the template name.
        Notes: you can use the *template_name* attribute to override the default template name.
        """
        if getattr(self, "template_name", None):
            return self.template_name

        return f"apps/{self.get_app_label()}/update.html"

    def get_form_template_name(self) -> str:
        """
        Returns the form template name.
        Notes: you can use the *form_template_name* attribute to override the default form template name.
        """
        if getattr(self, "form_template_name", None):
            return self.form_template_name

        return "components/app-forms/update.html"

    def get_form_modal_template_name(self) -> str:
        """
        Returns the form modal template name.
        Notes: you can use the *form_modal_template_name* attribute to override the default form modal template name.
        """
        if getattr(self, "form_modal_template_name", None):
            return self.form_modal_template_name

        return "components/app-forms/modal-update.html"

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
        return {
            "index_url": reverse(f"{app_label}:index"),
            "update_url": self.obj.get_update_url(),
        }

    def get_html_ids(self) -> dict[str, str]:
        """
        Returns the html ids.
        """
        app_label = self.get_app_label()
        return {
            "form_id": f"{app_label}-form",
            "table_id": f"{app_label}-table",
        }

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """
        Returns the context data that will be passed to the template.
        """
        form = self.form_class(instance=self.obj)
        context = {
            "form": form,
            **self.get_app_urls(),
            **self.get_html_ids(),
        }
        return context
