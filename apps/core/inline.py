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

    custom_formset_class: BaseInlineFormSet | None = None
    extra: int = 200
    max_num: int = 200

    def get_formset_class(
        self, request: HttpRequest, parent_model: Model
    ) -> type[BaseInlineFormSet]:
        kwargs = {
            "parent_model": parent_model,
            "model": self.model,
            "form": self.form_class,
            "extra": self.extra,
            "fields": self.fields,
            "max_num": self.max_num,
            "can_delete": request.user.has_perm(self.can_delete_permission),
        }

        if self.custom_formset_class:
            kwargs["formset"] = self.custom_formset_class

        return inlineformset_factory(**kwargs)
