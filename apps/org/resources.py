from django.utils.translation import gettext as _
from import_export import fields

from apps.core.resources import BaseResource

from . import models


class JobTypeResource(BaseResource):
    class Meta:
        model = models.JobType


class JobSubtypeResource(BaseResource):
    job_type = fields.Field(
        attribute="job_type__name",
        column_name=_("job type").title(),
    )

    class Meta:
        model = models.JobSubtype
        fields = ("id", "name", "job_type", "description", "slug")


class GroupResource(BaseResource):
    class Meta:
        model = models.Group