from apps.core.filters import (
    BaseNameDescriptionFilter,
    FilterComboboxMixin,
)

from .. import models


class BaseYearsFilter(BaseNameDescriptionFilter):
    class Meta:
        model = models.Year
        fields = ("name", "description")


class APIYearsFilter(FilterComboboxMixin, BaseYearsFilter):
    pass


class YearFilter(FilterComboboxMixin, BaseYearsFilter):
    pass
