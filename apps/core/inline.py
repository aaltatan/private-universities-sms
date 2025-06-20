from abc import ABC, abstractmethod
from typing import Iterable

from django.contrib import messages
from django.db.models import Model
from django.forms import HiddenInput, ModelForm
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.http import HttpRequest

from apps.core.utils.behaviors import ActionBehavior


class CustomBaseInlineFormSet(ABC, BaseInlineFormSet):
    @abstractmethod
    def delete_existing(self, obj, commit=True):
        pass


class InlineFormset(CustomBaseInlineFormSet):
    ordering_widget = HiddenInput

    def delete_existing(self, obj, commit=True):
        if commit:
            deleter = self.deleter_class(self.request, obj=obj)
            deleter.action()
            message = deleter.get_message()

            if deleter.has_executed:
                messages.success(self.request, message)
            else:
                messages.error(self.request, message)


class InlineFormsetFactory(ABC):
    @property
    @abstractmethod
    def model(self) -> type[ModelForm]:
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
    def deleter(self) -> ActionBehavior:
        pass

    custom_formset_class: InlineFormset | None = None
    max_num: int = 1000

    @property
    def app_label(self) -> str:
        return self.model._meta.app_label

    @property
    def codename_plural(self) -> str:
        return self.model._meta.codename_plural

    @property
    def object_name(self) -> str:
        return self.model._meta.object_name.lower()

    @property
    def add_permission(self) -> str:
        return f"{self.app_label}.add_{self.object_name}"

    @property
    def change_permission(self) -> str:
        return f"{self.app_label}.change_{self.object_name}"

    @abstractmethod
    def get_queryset(self, obj: Model):
        pass

    def get_inline_formset_class(self, request: HttpRequest) -> type[InlineFormset]:
        if self.custom_formset_class:
            inline_class = self.custom_formset_class
        else:
            inline_class = InlineFormset

        inline_class.deleter_class = self.deleter
        inline_class.request = request

        return inline_class

    def get_formset_class(
        self,
        request: HttpRequest,
        parent_model: Model,
        max_num: int | None = None,
    ) -> type[InlineFormset]:
        kwargs = {
            "parent_model": parent_model,
            "model": self.model,
            "form": self.form_class,
            "extra": 0,
            "fields": self.fields,
            "can_order": True,
            "max_num": max_num if max_num is not None else self.max_num,
            "formset": self.get_inline_formset_class(request),
            "can_delete": request.user.has_perm(
                f"{self.app_label}.delete_{self.object_name}",
            ),
        }

        return inlineformset_factory(**kwargs)
