import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import FilterTextMixin, get_text_filter

from .. import models


class BaseEmailFilter(FilterTextMixin, filters.FilterSet):
    email = get_text_filter(label=_("email"))

    class Meta:
        model = models.Email
        fields = ("email", "kind", "notes")


class APIEmailFilter(BaseEmailFilter):
    pass


class EmailFilter(BaseEmailFilter):
    pass
