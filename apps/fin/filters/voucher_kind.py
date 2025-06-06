from apps.core.filters import (
    BaseNameDescriptionFilter,
    FilterComboboxMixin,
)

from .. import models


class BaseVoucherKindsFilter(BaseNameDescriptionFilter):
    class Meta:
        model = models.VoucherKind
        fields = ("name", "description")


class APIVoucherKindsFilter(FilterComboboxMixin, BaseVoucherKindsFilter):
    pass


class VoucherKindFilter(FilterComboboxMixin, BaseVoucherKindsFilter):
    pass
