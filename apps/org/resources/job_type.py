from django.utils.translation import gettext_lazy as _
from import_export import fields

from apps.core.resources import BaseResource

from .. import models


class JobTypeResource(BaseResource):
    job_subtypes_count = fields.Field(
        attribute="job_subtypes_count",
        column_name=_("job subtypes count"),
    )
    employees_count = fields.Field(
        attribute="employees_count",
        column_name=_("employees count"),
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
