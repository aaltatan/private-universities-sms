from apps.core.resources import BaseResource

from .. import models


class YearResource(BaseResource):
    class Meta:
        model = models.Year
        fields = ("serial", "name", "description", "slug")
