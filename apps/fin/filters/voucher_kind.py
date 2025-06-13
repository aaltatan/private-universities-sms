from apps.core.filters import (
    BaseNameDescriptionFilter,
    FilterComboboxMixin,
)

from .. import models


class BaseVoucherKindFilter(BaseNameDescriptionFilter):
    class Meta:
        model = models.VoucherKind
        fields = ("name", "description")


class APIVoucherKindFilter(FilterComboboxMixin, BaseVoucherKindFilter):
    pass


class VoucherKindFilter(FilterComboboxMixin, BaseVoucherKindFilter):
    pass
