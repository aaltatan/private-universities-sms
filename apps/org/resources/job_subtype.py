from django.utils.translation import gettext_lazy as _
from import_export import fields

from apps.core.resources import BaseResource

from .. import models


class JobSubtypeResource(BaseResource):
    job_type = fields.Field(
        attribute="job_type__name",
        column_name=_("job type"),
    )
    employees_count = fields.Field(
        attribute="employees_count",
        column_name=_("employees count"),
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
