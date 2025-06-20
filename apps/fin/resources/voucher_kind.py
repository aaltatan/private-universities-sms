from apps.core.resources import BaseResource

from .. import models


class VoucherKindResource(BaseResource):
    class Meta:
        model = models.VoucherKind
        fields = ("serial", "name", "description", "slug")
