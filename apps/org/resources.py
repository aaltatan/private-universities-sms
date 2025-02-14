from apps.core.resources import BaseResource

from . import models


class JobTypeResource(BaseResource):
    class Meta:
        model = models.JobType