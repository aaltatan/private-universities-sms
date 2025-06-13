from apps.core.filters import (
    BaseNameDescriptionFilter,
    FilterComboboxMixin,
)

from .. import models


class BaseYearFilter(BaseNameDescriptionFilter):
    class Meta:
        model = models.Year
        fields = ("name", "description")


class APIYearFilter(FilterComboboxMixin, BaseYearFilter):
    pass


class YearFilter(FilterComboboxMixin, BaseYearFilter):
    pass
