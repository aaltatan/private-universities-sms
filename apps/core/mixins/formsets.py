from abc import ABC, abstractmethod
from typing import Iterable

from django.contrib import messages
from django.db.models import Model
from django.forms import ModelForm
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext as _


class FormsetMixin(ABC):
    @property
    @abstractmethod
    def parent_model(self) -> type[Model]:
        pass

    @property
    @abstractmethod
    def model(self) -> type[Model]:
        pass

    @property
    @abstractmethod
    def form_class(self) -> type[ModelForm]:
        pass

    @property
    @abstractmethod
    def fields(self) -> Iterable[str]:
        pass

    @property
    @abstractmethod
    def can_delete_permission(self) -> str:
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
    custom_formset_class: BaseInlineFormSet | None = None
    extra: int = 1
    max_num: int = 200

    def get(self, request: HttpRequest, slug: str, *args, **kwargs) -> HttpResponse:
        self.obj = get_object_or_404(self.parent_model, slug=slug)
        Formset = self.get_formset_class()
        formset = Formset(
            instance=self.obj,
            queryset=self.get_queryset(),
        )

        context = self.get_context_data(formset=formset)

        template_name = self.get_template_name()

        if request.htmx:
            template_name = self.get_form_template_name()

        return render(request, template_name, context)

    def post(self, request: HttpRequest, slug: str, *args, **kwargs) -> HttpResponse:
        self.obj = get_object_or_404(self.parent_model, slug=slug)
        Formset = self.get_formset_class()
        formset = Formset(request.POST, instance=self.obj)

        if formset.is_valid():
            formset.save()
            messages.success(request, self.get_success_message())
            formset = Formset(
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

    def get_formset_class(self) -> type[BaseInlineFormSet]:
        kwargs = {
            "parent_model": self.parent_model,
            "model": self.model,
            "form": self.form_class,
            "extra": self.extra,
            "can_delete": False,
            "fields": self.fields,
            "max_num": self.max_num,
        }

        if self.request.user.has_perm(self.can_delete_permission):
            kwargs["can_delete"] = True

        if self.custom_formset_class:
            kwargs["formset"] = self.custom_formset_class

        return inlineformset_factory(**kwargs)

    def get_success_message(self) -> str:
        if self.success_message:
            return self.success_message

        return _("objects has been updated successfully")

    def get_error_message(self) -> str:
        if self.error_message:
            return self.error_message

        return _("error while updating objects")

    def get_verbose_name_plural(self) -> str:
        return self.parent_model._meta.verbose_name_plural

    def get_app_label(self) -> str:
        return self.parent_model._meta.app_label

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
            "form_id": f"{self.verbose_name_plural}",
            **kwargs,
        }
