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
    def app_label(cls) -> str:
        return cls.model._meta.app_label

    @property
    def object_name(cls) -> str:
        return cls.model._meta.object_name.lower()

    @classmethod
    def get_queryset(cls, obj: Model):
        pass

    @classmethod
    def get_formset_class(
        cls,
        request: HttpRequest,
        parent_model: Model,
        extra: int | None = None,
        max_num: int | None = None,
    ) -> type[BaseInlineFormSet]:
        kwargs = {
            "parent_model": parent_model,
            "model": cls.model,
            "form": cls.form_class,
            "extra": extra and cls.extra,
            "fields": cls.fields,
            "max_num": max_num and cls.max_num,
            "can_delete": request.user.has_perm(
                f"{cls.app_label}.delete_{cls.object_name}",
            ),
        }

        if cls.custom_formset_class:
            kwargs["formset"] = cls.custom_formset_class

        return inlineformset_factory(**kwargs)
