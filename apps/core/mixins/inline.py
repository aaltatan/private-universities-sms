from abc import ABC, abstractmethod

from django.contrib import messages
from django.db.models import Model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext as _
from django.forms.models import BaseInlineFormSet


class InlineMixin(ABC):
    @property
    @abstractmethod
    def formset(self) -> type[BaseInlineFormSet]:
        pass

    @property
    @abstractmethod
    def model(self) -> type[Model]:
        pass

    @property
    @abstractmethod
    def verbose_name_plural(self) -> str:
        pass

    @abstractmethod
    def get_queryset(self):
        pass

    success_message: str | None = None
    error_message: str | None = None
    template_name: str | None = None
    form_template_name: str | None = None

    def get(self, request: HttpRequest, slug: str, *args, **kwargs) -> HttpResponse:
        self.obj = get_object_or_404(self.model, slug=slug)
        formset = self.formset(
            instance=self.obj,
            queryset=self.get_queryset(),
        )

        context = self.get_context_data(formset=formset)
        template_name = self.get_template_name()

        return render(request, template_name, context)

    def post(self, request: HttpRequest, slug: str, *args, **kwargs) -> HttpResponse:
        self.obj = get_object_or_404(self.model, slug=slug)
        formset = self.formset(request.POST, instance=self.obj)

        if formset.is_valid():
            formset.save()
            messages.success(request, self.get_success_message())
            formset = self.formset(
                instance=self.obj,
                queryset=self.get_queryset(),
            )
        else:
            messages.error(request, self.get_error_message())

        context = self.get_context_data(formset=formset)
        template_name = self.get_form_template_name()

        response = render(request, template_name, context)
        response["Hx-Trigger"] = "messages"

        return response

    def get_success_message(self) -> str:
        if self.success_message:
            return self.success_message

        return _("objects has been updated successfully")

    def get_error_message(self) -> str:
        if self.error_message:
            return self.error_message

        return _("error while updating objects")

    def get_verbose_name_plural(self) -> str:
        return self.model._meta.verbose_name_plural

    def get_app_label(self) -> str:
        return self.model._meta.app_label

    def get_template_name(self) -> str:
        if self.template_name:
            return self.template_name

        verbose_name_plural = self.get_verbose_name_plural()
        app_label = self.get_app_label()

        return f"apps/{app_label}/{verbose_name_plural}/inlines/{self.verbose_name_plural}.html"

    def get_form_template_name(self) -> str:
        if self.form_template_name:
            return self.form_template_name

        verbose_name_plural = self.get_verbose_name_plural()
        app_label = self.get_app_label()

        return f"components/{app_label}/{verbose_name_plural}/inlines/{self.verbose_name_plural}.html"

    def get_context_data(self, **kwargs) -> dict[str, str]:
        return {
            "object": self.obj,
            **kwargs,
        }
