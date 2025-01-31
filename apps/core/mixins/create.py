from abc import ABC, abstractmethod
from typing import Any

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext as _

from ..models import Activity
from ..schemas import RequestParser


class CreateMixin(ABC):
    """
    A mixin that adds a create form.
    """

    @property
    @abstractmethod
    def form_class(self) -> type[ModelForm]:
        pass

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Handles GET requests and returns a rendered template.
        """
        request_parser = RequestParser(
            request=request,
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
        form = self.form_class(request.POST)
        request_parser = RequestParser(
            request=request,
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

        return response

    def get_form_valid_response(
        self,
        request: HttpRequest,
        form: type[ModelForm],
        request_parser: RequestParser,
    ) -> HttpResponse:
        """
        Returns the form valid response.
        """
        obj = form.save()
        Activity.objects.create(
            user=request.user,
            kind=Activity.KindChoices.CREATE,
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.pk,
        )
        messages.success(
            request,
            _("{} has been created successfully").format(obj),
        )

        response = HttpResponse(status=201)

        if request_parser.target == "#no-content":
            response["Hx-Reswap"] = "innerHTML"

        if request.POST.get("save"):
            if not request_parser.dont_redirect:
                if request_parser.is_modal_request:
                    response["Hx-Location"] = request_parser.hx_location
                else:
                    response["Hx-Redirect"] = request_parser.index_url
        elif request.POST.get("save_and_add_another"):
            context = self.get_context_data()
            response = render(
                request=request,
                template_name=self.get_form_template_name(),
                context=context,
                status=201,
            )
        else:
            raise ValueError("save or save_and_add_another is required")

        response["Hx-Trigger"] = "messages"
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

        return f"apps/{self.get_app_label()}/create.html"

    def get_form_modal_template_name(self) -> str:
        """
        Returns the form modal template name.
        Notes: you can use the *form_modal_template_name* attribute to override the default form modal template name.
        """
        app_label = self.get_app_label()

        if getattr(self, "form_modal_template_name", None):
            return self.form_modal_template_name

        return f"components/{app_label}/modal-create.html"

    def get_form_template_name(self) -> str:
        """
        Returns the form template name.
        Notes: you can use the *form_template_name* attribute to override the default form template name.
        """
        app_label = self.get_app_label()

        if getattr(self, "form_template_name", None):
            return self.form_template_name

        return f"components/{app_label}/create.html"

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
            "create_url": reverse(f"{app_label}:create"),
        }

    def get_html_ids(self) -> dict[str, str]:
        """
        Returns the html ids.
        """
        app_label = self.get_app_label()
        return {
            "table_id": f"{app_label}-table",
            "form_id": f"{app_label}-form",
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
