from django.db.models import Q, QuerySet

from ..utils import get_djangoql_query, get_keywords_query


class FilterTextMixin:
    """
    A mixin that adds a text filter to a model.
    """

    def filter_text(self, qs, name, value):
        if not value:
            return qs

        is_reversed = value.startswith("!")

        if is_reversed:
            value = value[1:]

        query = get_keywords_query(
            value,
            field_name=name,
            is_reversed=is_reversed,
        )
        return qs.filter(query)


class FilterComboboxMixin:
    """
    A mixin that add a filter_combobox to a model.
    """

    def filter_combobox_combined(self, qs, name, value):
        if not value:
            return qs

        for obj in value:
            qs = qs.filter(**{name: obj})

        return qs

    def filter_combobox(self, qs, name, value):
        if not value:
            return qs

        stmt = Q(**{f"{name}__in": value})

        return qs.filter(stmt).distinct()


class FilterSearchMixin:
    """
    A mixin that adds a search filter to a model.
    """

    def search(
        self,
        queryset: QuerySet,
        name: str,
        value: str,
    ) -> QuerySet:
        """
        Searches the queryset for the given name and value.
        """
        default_queryset = queryset.filter(get_keywords_query(value))
        return get_djangoql_query(queryset, value, default_queryset)
