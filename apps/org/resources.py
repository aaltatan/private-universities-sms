from django.utils.translation import gettext as _
from import_export import fields

from apps.core.resources import BaseResource

from . import models


class JobTypeResource(BaseResource):
    job_subtypes_count = fields.Field(
        attribute="job_subtypes_count",
        column_name=_("job subtypes count").title(),
    )

    class Meta:
        model = models.JobType
        fields = (
            "serial",
            "name",
            "job_subtypes_count",
            "description",
            "slug",
        )


class JobSubtypeResource(BaseResource):
    job_type = fields.Field(
        attribute="job_type__name",
        column_name=_("job type").title(),
    )

    class Meta:
        model = models.JobSubtype
        fields = ("serial", "name", "job_type", "description", "slug")


class GroupResource(BaseResource):
    class Meta:
        model = models.Group
        fields = ("serial", "name", "description", "slug")


class CostCenterResource(BaseResource):
    accounting_id = fields.Field(
        attribute="accounting_id",
        column_name=_("accounting id").title(),
    )

    class Meta:
        model = models.CostCenter
        fields = ("serial", "name", "accounting_id", "description", "slug")


class PositionResource(BaseResource):
    order = fields.Field(
        attribute="order",
        column_name=_("order").title(),
    )

    class Meta:
        model = models.Position
        fields = ("serial", "name", "order", "description", "slug")


class StatusResource(BaseResource):
    is_payable = fields.Field(
        attribute="is_payable",
        column_name=_("is payable").title(),
    )

    def dehydrate_is_payable(self, obj: models.Status):
        return self._dehydrate_boolean(obj.is_payable)

    class Meta:
        model = models.Status
        fields = ("serial", "name", "is_payable", "description", "slug")


class DepartmentResource(BaseResource):
    parent = fields.Field(
        attribute="parent__name",
        column_name=_("parent").title(),
    )
    cost_center = fields.Field(
        attribute="cost_center__name",
        column_name=_("cost center").title(),
    )
    kind = fields.Field(
        attribute="kind",
        column_name=_("kind").title(),
    )

    def dehydrate_name(self, obj: models.Department):
        return obj.name.rjust(len(obj.name) + obj.get_level() * 4)

    def dehydrate_kind(self, obj: models.Department):
        kind = _("child") if obj.is_leaf_node() else _("parent")
        return kind.title()

    class Meta:
        model = models.Department
        fields = (
            "serial",
            "name",
            "kind",
            "parent",
            "cost_center",
            "description",
            "slug",
        )
