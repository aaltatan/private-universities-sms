from django.core.paginator import InvalidPage
from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.utils.urls import replace_query_param



class CorePagination(PageNumberPagination):
    page_size = settings.PER_PAGE
    page_size_query_param = "per_page"
    max_page_size = settings.MAX_PAGE_SIZE

    def get_current_link(self):
        url = self.request.build_absolute_uri()
        page_number = self.page.number
        return replace_query_param(url, self.page_query_param, page_number)

    def get_page_size(self, request: Request):
        page_size = request.query_params.get("per_page")

        if not page_size:
            return self.page_size

        if page_size.lower() == "all":
            return self.max_page_size

        return page_size

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        self.request = request
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = self.get_page_number(request, paginator)

        try:
            self.page = paginator.page(page_number)
        except InvalidPage:
            self.page = paginator.page(1)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        return list(self.page)
