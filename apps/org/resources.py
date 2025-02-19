from django.utils.translation import gettext as _
from import_export import fields

from apps.core.resources import BaseResource

from . import models


class JobTypeResource(BaseResource):
    class Meta:
        model = models.JobType
        fields = ("serial", "name", "description", "slug")


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

    def dehydrate_is_payable(self, value: bool):
        return _("yes").title() if value else _("no").title()

    class Meta:
        model = models.Status
        fields = ("serial", "name", "is_payable", "description", "slug")
