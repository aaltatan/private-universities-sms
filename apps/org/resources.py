from django.utils.translation import gettext as _
from import_export import fields

from apps.core.resources import BaseResource

from . import models


class JobTypeResource(BaseResource):
    job_subtypes_count = fields.Field(
        attribute="job_subtypes_count",
        column_name=_("job subtypes count").title(),
    )
    employees_count = fields.Field(
        attribute="employees_count",
        column_name=_("employees count").title(),
    )

    class Meta:
        model = models.JobType
        fields = (
            "serial",
            "name",
            "job_subtypes_count",
            "employees_count",
            "description",
            "slug",
        )


class JobSubtypeResource(BaseResource):
    job_type = fields.Field(
        attribute="job_type__name",
        column_name=_("job type").title(),
    )
    employees_count = fields.Field(
        attribute="employees_count",
        column_name=_("employees count").title(),
    )

    class Meta:
        model = models.JobSubtype
        fields = (
            "serial",
            "name",
            "job_type",
            "employees_count",
            "description",
            "slug",
        )


class GroupResource(BaseResource):
    kind = fields.Field(
        attribute="kind",
        column_name=_("kind").title(),
    )
    employees_count = fields.Field(
        attribute="employees_count",
        column_name=_("employees count").title(),
    )

    def dehydrate_kind(self, obj: models.Group):
        return self._dehydrate_choices(obj, "kind")

    class Meta:
        model = models.Group
        fields = (
            "serial",
            "name",
            "kind",
            "employees_count",
            "description",
            "slug",
        )


class CostCenterResource(BaseResource):
    accounting_id = fields.Field(
        attribute="accounting_id",
        column_name=_("accounting id").title(),
    )
    employees_count = fields.Field(
        attribute="employees_count",
        column_name=_("employees count").title(),
    )

    class Meta:
        model = models.CostCenter
        fields = (
            "serial",
            "name",
            "accounting_id",
            "employees_count",
            "description",
            "slug",
        )


class PositionResource(BaseResource):
    order = fields.Field(
        attribute="order",
        column_name=_("order").title(),
    )
    employees_count = fields.Field(
        attribute="employees_count",
        column_name=_("employees count").title(),
    )

    class Meta:
        model = models.Position
        fields = (
            "serial",
            "name",
            "order",
            "employees_count",
            "description",
            "slug",
        )


class StatusResource(BaseResource):
    is_payable = fields.Field(
        attribute="is_payable",
        column_name=_("is payable").title(),
    )
    employees_count = fields.Field(
        attribute="employees_count",
        column_name=_("employees count").title(),
    )

    def dehydrate_is_payable(self, obj: models.Status):
        return self._dehydrate_boolean(obj.is_payable)

    class Meta:
        model = models.Status
        fields = (
            "serial",
            "name",
            "is_payable",
            "employees_count",
            "description",
            "slug",
        )
