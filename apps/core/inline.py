from abc import ABC, abstractmethod
from typing import Iterable

from django.db.models import Model
from django.forms import ModelForm
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.http import HttpRequest


class InlineFormsetFactory(ABC):
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

    @classmethod
    def get_queryset(cls, obj: Model):
        pass

    custom_formset_class: BaseInlineFormSet | None = None
    extra: int = 1
    max_num: int = 1000

    @classmethod
    def get_formset_class(
        cls, request: HttpRequest, parent_model: Model
    ) -> type[BaseInlineFormSet]:
        kwargs = {
            "parent_model": parent_model,
            "model": cls.model,
            "form": cls.form_class,
            "extra": cls.extra,
            "fields": cls.fields,
            "max_num": cls.max_num,
            "can_delete": request.user.has_perm(cls.can_delete_permission),
        }

        if cls.custom_formset_class:
            kwargs["formset"] = cls.custom_formset_class

        return inlineformset_factory(**kwargs)
