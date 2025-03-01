import json
from abc import ABC, abstractmethod
from typing import Any

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model
from django.forms import BaseInlineFormSet, ModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import gettext as _
from rest_framework.serializers import ModelSerializer

from ..inline import InlineFormsetFactory
from ..models import Activity
from ..schemas import RequestParser
from ..utils import get_differences


class UpdateMixin(ABC):
    """
    A mixin that adds an update form.
    """

    @property
    @abstractmethod
    def form_class(self) -> type[ModelForm]:
        pass

    @property
    @abstractmethod
    def activity_serializer(self) -> type[ModelSerializer]:
        pass

    template_name: str | None = None
    form_template_name: str | None = None
    form_modal_template_name: str | None = None
    inlines: dict[str, InlineFormsetFactory] | None = None

    def get(self, request: HttpRequest, slug: str, *args, **kwargs) -> HttpResponse:
        """
        Handles GET requests and returns a rendered template.
        """
        self.obj = get_object_or_404(self.get_model_class(), slug=slug)

        request_parser = RequestParser(
            request=request,
            action="update",
            index_url=self.get_app_urls()["index_url"],
        )

        template_name = self.get_template_name()
        formsets_context = self.get_formsets_context(self.obj)
        context = self.get_context_data(**formsets_context)

        if request.htmx:
            if request_parser.is_modal_request:
                context["request_parser"] = request_parser.asdict()
                template_name = self.get_form_modal_template_name()
            else:
                template_name = self.get_form_template_name()

        return render(request, template_name, context)

    def post(self, request: HttpRequest, slug: str, *args, **kwargs) -> HttpResponse:
        """
        Handles the POST request.
        """
        model = self.get_model_class()
        self.obj = get_object_or_404(model, slug=slug)

        from_data: dict | list = self.activity_serializer(self.obj).data

        form = self.form_class(request.POST, instance=self.obj)

        formsets = []
        if self.inlines:
            for inline_class in self.inlines.values():
                inline: InlineFormsetFactory = inline_class()
                qs = inline.get_queryset(self.obj)
                Formset = inline.get_formset_class(
                    request=request, parent_model=self.get_model_class()
                )
                formset = Formset(
                    request.POST,
                    instance=self.obj,
                    queryset=qs,
                )
                formsets.append(formset)

        request_parser = RequestParser(
            request=request,
            action="update",
            index_url=self.get_app_urls()["index_url"],
        )
        if form.is_valid() and all(formset.is_valid() for formset in formsets):
            return self.get_form_valid_response(
                request=request,
                form=form,
                request_parser=request_parser,
                from_data=from_data,
                formsets=formsets,
            )

        return self.get_form_invalid_response(
            request=request,
            form=form,
            request_parser=request_parser,
        )

    def get_form_valid_response(
        self,
        request: HttpRequest,
        form: type[ModelForm],
        request_parser: RequestParser,
        from_data: dict | list,
        formsets: list[BaseInlineFormSet],
    ) -> HttpResponse:
        """
        Returns the form valid response.
        """
        obj = form.save()
        for formset in formsets:
            formset.save()

        to_data: dict | list = self.activity_serializer(obj).data
        differences = get_differences(from_data, to_data)

        if differences:
            Activity.objects.create(
                user=request.user,
                kind=Activity.KindChoices.UPDATE,
                content_type=ContentType.objects.get_for_model(self.obj),
                object_id=self.obj.pk,
                data=differences,
            )

        messages.success(
            request,
            _("({}) has been updated successfully").format(obj),
        )

        response = HttpResponse(status=200)

        if request_parser.target == "#no-content":
            response["Hx-Reswap"] = "innerHTML"

        if not request_parser.dont_redirect:
            if request_parser.is_modal_request:
                response["Hx-Location"] = request_parser.hx_location
            else:
                if request_parser.update:
                    response["Hx-Redirect"] = request_parser.index_url
                elif request_parser.update_and_continue_editing:
                    template_name = self.get_form_template_name()
                    formsets_context = self.get_formsets_context(obj)
                    context = self.get_context_data(**formsets_context)
                    response = render(request, template_name, context)

        response["Hx-Trigger"] = "messages"

        if request_parser.is_modal_request:
            response["Hx-Trigger"] = json.dumps(
                {
                    "hidemodal": "hiding modal after success request",
                    "messages": "getting messages",
                },
            )

        return response

    def get_form_invalid_response(
        self,
        request: HttpRequest,
        form: type[ModelForm],
        request_parser: RequestParser,
    ) -> HttpResponse:
        """
        Returns the form invalid response.
        """
        template_name = self.get_form_template_name()

        formset_context = self.get_formsets_context(self.obj, include_data=True)
        context = self.get_context_data(**formset_context)
        context["form"] = form

        if request_parser.is_modal_request:
            template_name = self.get_form_modal_template_name()
            context["update_url"] = request.path
            response = render(request, template_name, context)
            response["Hx-Retarget"] = "#modal-container"
        else:
            response = render(request, template_name, context)
        return response

    def get_formsets_context(
        self, obj: Model, include_data: bool = False
    ) -> dict[str, BaseInlineFormSet]:
        context = {}

        if self.inlines:
            for app_label, inline_class in self.inlines.items():
                key = f"{app_label}_formset"

                extra: int | None = None

                inline: InlineFormsetFactory = inline_class()

                add_permission = f"{inline.app_label}.add_{inline.object_name}"
                change_permission = f"{inline.app_label}.change_{inline.object_name}"

                if not self.request.user.has_perm(add_permission):
                    extra = 0

                Formset = inline.get_formset_class(
                    request=self.request,
                    parent_model=self.get_model_class(),
                    extra=extra,
                )

                kwargs = {"instance": obj, "queryset": inline.get_queryset(obj)}

                if include_data:
                    kwargs["data"] = self.request.POST

                if self.request.user.has_perm(change_permission):
                    context[key] = Formset(**kwargs)

        return context

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

        verbose_name_plural = self.get_verbose_name_plural()
        app_label = self.get_app_label()

        return f"apps/{app_label}/{verbose_name_plural}/update.html"

    def get_form_template_name(self) -> str:
        """
        Returns the form template name.
        Notes: you can use the *form_template_name* attribute to override the default form template name.
        """
        verbose_name_plural = self.get_verbose_name_plural()
        app_label = self.get_app_label()

        if getattr(self, "form_template_name", None):
            return self.form_template_name

        return f"components/{app_label}/{verbose_name_plural}/update.html"

    def get_form_modal_template_name(self) -> str:
        """
        Returns the form modal template name.
        Notes: you can use the *form_modal_template_name* attribute to override the default form modal template name.
        """
        verbose_name_plural = self.get_verbose_name_plural()
        app_label = self.get_app_label()

        if getattr(self, "form_modal_template_name", None):
            return self.form_modal_template_name

        return f"components/{app_label}/{verbose_name_plural}/modal-update.html"

    def get_verbose_name_plural(self) -> str:
        """
        Returns the verbose name plural using the model.
        """
        model = self.get_model_class()
        return model._meta.verbose_name_plural

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
        app_label = self.get_verbose_name_plural()
        return {
            "index_url": reverse(f"{app_label}:index"),
            "update_url": self.obj.get_update_url(),
        }

    def get_html_ids(self) -> dict[str, str]:
        """
        Returns the html ids.
        """
        app_label = self.get_verbose_name_plural()
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
            **kwargs,
        }
        return context
