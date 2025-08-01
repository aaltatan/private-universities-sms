import json
from abc import ABC, abstractmethod
from typing import Any, Iterable

from django.contrib import messages
from django.db.models import Model
from django.forms import BaseInlineFormSet, ModelForm
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseRedirect,
)
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import gettext as _

from ..inline import InlineFormsetFactory
from ..schemas import RequestParser


class UpdateMixin(ABC):
    """
    A mixin that adds an update form.
    """

    @property
    @abstractmethod
    def form_class(self) -> type[ModelForm]:
        pass

    template_name: str | None = None
    form_template_name: str | None = None
    form_modal_template_name: str | None = None
    inlines: Iterable[InlineFormsetFactory] | None = None

    def get(self, request: HttpRequest, slug: str, *args, **kwargs) -> HttpResponse:
        """
        Handles GET requests and returns a rendered template.
        """
        self.obj = get_object_or_404(self.get_model_class(), slug=slug)

        if self.can_access(request=request, obj=self.obj) is False:
            messages.error(
                request,
                self.cannot_access_message(
                    request=request,
                    obj=self.obj,
                ),
            )
            referer = request.META.get("HTTP_REFERER")
            return HttpResponseRedirect(referer)

        request_parser = RequestParser(
            request=request,
            action="update",
            index_url=self.get_app_urls()["index_url"],
        )

        template_name = self.get_template_name()
        formsets_context = self.get_formsets_context(self.obj)
        context = self.get_context_data(instance=self.obj, **formsets_context)

        if request.htmx:
            if request_parser.is_modal_request:
                context["request_parser"] = request_parser.asdict()
                template_name = self.get_form_modal_template_name()
                response = render(request, template_name, context)
                response["Hx-Trigger"] = "showmodal"
                return response
            else:
                template_name = self.get_form_template_name()

        return render(request, template_name, context)

    def post(self, request: HttpRequest, slug: str, *args, **kwargs) -> HttpResponse:
        """
        Handles the POST request.
        """
        model = self.get_model_class()
        self.obj = get_object_or_404(model, slug=slug)

        form = self.form_class(
            request.POST,
            request.FILES,
            instance=self.obj,
        )

        request_parser = RequestParser(
            request=request,
            action="update",
            index_url=self.get_app_urls()["index_url"],
        )

        formsets: list[BaseInlineFormSet] = []
        if self.inlines and not request_parser.is_modal_request:
            for inline_class in self.inlines:
                inline: InlineFormsetFactory = inline_class()
                qs = inline.get_queryset(self.obj)
                Formset = inline.get_formset_class(
                    request=request, parent_model=self.get_model_class()
                )
                formset = Formset(request.POST, instance=self.obj, queryset=qs)
                formsets.append(formset)

        # performance issue
        if form.is_valid() and all(formset.is_valid() for formset in formsets):
            for formset in formsets:
                new_objects = [
                    item for item in formset.cleaned_data if not item.get("id") and item
                ]
                criteria = bool(new_objects) and not request.user.has_perm(
                    inline.add_permission
                )
                if criteria:
                    return HttpResponseForbidden()

            return self.get_form_valid_response(
                request=request,
                form=form,
                request_parser=request_parser,
                formsets=formsets,
            )

        return self.get_form_invalid_response(
            request=request,
            form=form,
            request_parser=request_parser,
        )

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

    def perform_update(
        self,
        form: ModelForm,
        formsets: list[BaseInlineFormSet],
    ) -> Any:
        """
        action for performing update.
        """
        obj = form.save()
        for formset in formsets:
            last_order = 1
            for form in formset.forms:
                if form.has_changed():
                    if form.is_valid() and form.cleaned_data:
                        item = form.save(commit=False)
                        item.ordering = form.cleaned_data.get("ORDER") or last_order
                        item.save()
                        last_order += 1
            if formset.has_changed():
                formset.save()

        return obj

    def get_form_valid_response(
        self,
        request: HttpRequest,
        form: type[ModelForm],
        request_parser: RequestParser,
        formsets: list[BaseInlineFormSet],
    ) -> HttpResponse:
        """
        Returns the form valid response.
        """
        obj = self.perform_update(form=form, formsets=formsets)

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
                    context = self.get_context_data(
                        instance=obj,
                        **formsets_context,
                    )
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
        context = self.get_context_data(
            form=form,
            instance=form.instance,
            **formset_context,
        )

        if request_parser.is_modal_request:
            template_name = self.get_form_modal_template_name()
            context["update_url"] = request.path
            response = render(request, template_name, context)
            response["Hx-Retarget"] = "#modal-container"
        else:
            response = render(request, template_name, context)

        messages.error(request, _("form is invalid"))
        response["Hx-Trigger"] = "messages"

        return response

    def get_formsets_context(
        self, obj: Model, include_data: bool = False
    ) -> dict[str, BaseInlineFormSet]:
        context = {}

        if self.inlines:
            for inline_class in self.inlines:
                inline: InlineFormsetFactory = inline_class()
                key = f"{inline.codename_plural}_formset"

                Formset = inline.get_formset_class(
                    request=self.request,
                    parent_model=self.get_model_class(),
                )

                kwargs = {
                    "instance": obj,
                    "queryset": inline.get_queryset(obj),
                }

                if include_data:
                    kwargs["data"] = self.request.POST

                if self.request.user.has_perm(inline.change_permission):
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

        codename_plural = self.get_codename_plural()
        app_label = self.get_app_label()

        return f"apps/{app_label}/{codename_plural}/update.html"

    def get_form_template_name(self) -> str:
        """
        Returns the form template name.
        Notes: you can use the *form_template_name* attribute to override the default form template name.
        """
        codename_plural = self.get_codename_plural()
        app_label = self.get_app_label()

        if getattr(self, "form_template_name", None):
            return self.form_template_name

        return f"components/{app_label}/{codename_plural}/update.html"

    def get_form_modal_template_name(self) -> str:
        """
        Returns the form modal template name.
        Notes: you can use the *form_modal_template_name* attribute to override the default form modal template name.
        """
        codename_plural = self.get_codename_plural()
        app_label = self.get_app_label()

        if getattr(self, "form_modal_template_name", None):
            return self.form_modal_template_name

        return f"components/{app_label}/{codename_plural}/modal-update.html"

    def get_codename_plural(self) -> str:
        """
        Returns the codename plural using the model.
        """
        model = self.get_model_class()
        return model._meta.codename_plural

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
            "update_url": self.obj.get_update_url(),
        }

    def get_html_ids(self) -> dict[str, str]:
        """
        Returns the html ids.
        """
        app_label = self.get_codename_plural()
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
