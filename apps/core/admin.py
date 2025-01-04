from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from djangoql.admin import DjangoQLSearchMixin, apply_search

from .models import User


class CustomDjangoQLSearchMixin(DjangoQLSearchMixin):
    def get_search_results(self, request, queryset, search_term):
        if not search_term:
            return queryset, False
        qs = apply_search(queryset, search_term, self.djangoql_schema)
        return qs, False


admin.site.register(User, UserAdmin)