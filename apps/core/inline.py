from abc import ABC, abstractmethod
from typing import Iterable

from django.db.models import Model
from django.forms import ModelForm
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.http import HttpRequest


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

    custom_formset_class: BaseInlineFormSet | None = None
    extra: int = 1
    max_num: int = 1000

    @property
    def app_label(self) -> str:
        return self.model._meta.app_label

    @property
    def object_name(self) -> str:
        return self.model._meta.object_name.lower()

    @abstractmethod
    def get_queryset(self, obj: Model):
        pass

    def get_formset_class(
        self,
        request: HttpRequest,
        parent_model: Model,
        extra: int | None = None,
        max_num: int | None = None,
    ) -> type[BaseInlineFormSet]:
        kwargs = {
            "parent_model": parent_model,
            "model": self.model,
            "form": self.form_class,
            "extra": extra if extra is not None else self.extra,
            "fields": self.fields,
            "max_num": max_num if max_num is not None else self.max_num,
            "can_delete": request.user.has_perm(
                f"{self.app_label}.delete_{self.object_name}",
            ),
        }

        if self.custom_formset_class:
            kwargs["formset"] = self.custom_formset_class

        return inlineformset_factory(**kwargs)
