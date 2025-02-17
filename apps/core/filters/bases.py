import django_filters as filters
from django.utils.translation import gettext_lazy as _

from .fields import get_text_filter
from .mixins import FilterSearchMixin, FilterTextMixin


class BaseNameDescriptionFilter(FilterTextMixin, filters.FilterSet):
    """
    a base class for filters that have **(name)** and **(description)** fields.
    """
    name = get_text_filter(label=_("name").title())
    description = get_text_filter(label=_("description").title())


class BaseQSearchFilter(FilterSearchMixin, filters.FilterSet):
    """
    a base class for filters that have a search field **(q)**.
    """
    q = filters.CharFilter(method="search")
