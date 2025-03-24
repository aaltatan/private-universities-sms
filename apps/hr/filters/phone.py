import django_filters as filters
from django.utils.translation import gettext_lazy as _

from apps.core.filters import FilterTextMixin, get_text_filter

from .. import models


class BasePhoneFilter(FilterTextMixin, filters.FilterSet):
    number = get_text_filter(label=_("number"))

    class Meta:
        model = models.Phone
        fields = ("number", "kind", "notes")


class APIPhoneFilter(BasePhoneFilter):
    pass


class PhoneFilter(BasePhoneFilter):
    pass
