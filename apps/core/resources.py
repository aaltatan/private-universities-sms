from typing import Any
from django.utils.translation import gettext as _
from import_export import fields, resources


class SerialResourceMixin:
    _serials: list[int] = []

    def dehydrate_serial(self, obj) -> int:
        if self._serials:
            value = self._serials[-1] + 1
        else:
            value = 1

        self._serials.append(value)
        return value


class DehydrateBooleanMixin:
    def _dehydrate_boolean(self, is_true: bool = True):
        return _("yes").title() if is_true else _("no").title()


class DehydrateChoicesMixin:
    def _dehydrate_choices(self, obj: Any, field_name: str) -> str:
        return getattr(obj, f"get_{field_name}_display")()


class BaseResource(
    SerialResourceMixin,
    DehydrateBooleanMixin,
    DehydrateChoicesMixin,
    resources.ModelResource,
):
    """
    Fields name, description, slug
    """

    serial = fields.Field(
        column_name="#",
        dehydrate_method="dehydrate_serial",
    )
    name = fields.Field(
        attribute="name",
        column_name=_("name").title(),
    )
    description = fields.Field(
        attribute="description",
        column_name=_("description").title(),
    )
    slug = fields.Field(
        attribute="slug",
        column_name=_("slug").title(),
    )
