from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Iterable, Literal

import django_filters as filters
from django.conf import settings
from django.core.paginator import EmptyPage, Page, PageNotAnInteger, Paginator
from django.db.models import Model, QuerySet
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseServerError,
)
from django.shortcuts import render
from django.urls import NoReverseMatch, reverse
from django_filters import FilterSet
from import_export.resources import ModelResource
from tablib import Dataset

from ..constants import PERMISSION
from ..filters import BaseQSearchFilter, get_ordering_filter
from ..schemas import Action


class TableFiltersMixin:
    def get_search_filter_class(self) -> type[FilterSet]:
        """
        Returns the search filter class.
        """
        if getattr(self, "search_filter_class", None):
            return self.search_filter_class

        class SearchFilter(BaseQSearchFilter):
            class Meta:
                model = self.get_model_class()
                fields = ("id",)

        return SearchFilter

    def get_ordering_filter_class(self) -> type[FilterSet]:
        """
        Returns the ordering filter class.
        """
        if getattr(self, "ordering_filter_class", None):
            return self.ordering_filter_class

        class OrderingFilter(filters.FilterSet):
            ordering = get_ordering_filter(self.ordering_fields)

            class Meta:
                model = self.get_model_class()
                fields = ("id",)

        return OrderingFilter


class TableVariablesMixin:
    def get_html_ids(self, verbose_name_plural: str) -> dict[str, str]:
        """
        Returns the html ids.
        """
        return {
            "table_id": f"{verbose_name_plural}-table",
            "form_table_id": f"{verbose_name_plural}-form-table",
            "filter_form_id": f"{verbose_name_plural}-filter",
        }

    def get_app_urls(self, app_label: str, verbose_name_plural: str) -> dict[str, str]:
        """
        Returns the app links.
        """
        # in case of no create view
        try:
            create_url = reverse(f"{app_label}:{verbose_name_plural}:create")
        except NoReverseMatch:
            create_url = None

        return {
            "index_url": reverse(f"{app_label}:{verbose_name_plural}:index"),
            "create_url": create_url,
        }

    def get_permissions(
        self, request: HttpRequest, app_label: str, object_name: str
    ) -> dict[str, bool]:
        """
        Returns a dictionary of permissions.
        """
        permissions: list[PERMISSION] = [
            "view",
            "add",
            "change",
            "delete",
            "export",
            "audit",
            "unaudit",
            "migrate",
            "unmigrate",
            "view_activity",
        ]
        return {
            f"can_{permission}": self._get_permission(
                request, permission, app_label, object_name
            )
            for permission in permissions
        }

    def _get_permission(
        self,
        request: HttpRequest,
        permission: PERMISSION,
        app_label: str,
        object_name: str,
    ) -> bool:
        """
        Returns whether the user has a given permission.
        """
        permission_string = f"{app_label}.{permission}_{object_name}"
        return request.user.has_perm(permission_string)


class PaginationMixin:
    def _get_per_page(self, request: HttpRequest) -> int:
        """
        Returns the number of items to show per page.
        """
        default_per_page: int = settings.PER_PAGE
        request_per_page: str = request.GET.get("per_page", None)

        if request_per_page == "all":
            return settings.MAX_PAGE_SIZE

        return request_per_page or default_per_page

    def get_page_class(self, request: HttpRequest, queryset: QuerySet) -> Page:
        """
        Returns the page class.
        """
        per_page = self._get_per_page(request=request)
        paginator = Paginator(queryset, per_page)
        page: int = request.GET.get("page", 1)

        try:
            page = paginator.page(page)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        return page


class ListMixin(PaginationMixin, TableVariablesMixin, TableFiltersMixin, ABC):
    """
    A mixin that adds a list view.
    """

    @property
    @abstractmethod
    def model(self) -> type[Model]:
        pass

    @property
    @abstractmethod
    def filter_class(self) -> type[FilterSet]:
        pass

    @property
    @abstractmethod
    def resource_class(self) -> type[ModelResource]:
        pass

    @property
    @abstractmethod
    def ordering_fields(self) -> Iterable[str]:
        pass

    @abstractmethod
    def get_actions(self) -> dict[str, Action]:
        pass

    queryset: QuerySet | None = None
    template_name: str | None = None
    table_template_name: str | None = None
    filter_form_template_name: str | None = None
    ordering_filter_class: type[FilterSet] | None = None
    search_filter_class: type[FilterSet] | None = None

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Handles GET requests and returns a rendered template.
        """
        if request.GET.get("redirected"):
            return self.get_export_response(request)

        if request.GET.get("filters"):
            return self.get_filters_response(request)

        template_name: str = self.get_template_name()

        if request.htmx:
            if request.GET.get("export") and not request.GET.get("redirected"):
                response = HttpResponse()
                response["Hx-Redirect"] = request.get_full_path() + "&redirected=true"
                return response
            template_name = self.get_table_template_name()

        context: dict[str, Any] = self.get_context_data()

        return render(request, template_name, context)

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Handles the POST request.
        """
        return self.get_bulk_actions_response(request)

    def get_filters_response(self, request: HttpRequest) -> HttpResponse:
        """
        Returns the filters response.
        """
        template_name = self.get_filter_form_template_name()
        context = self.filter_context_data()

        response = render(self.request, template_name, context)
        response["Hx-Trigger"] = "open-overlay-sidebar"

        return response

    def get_bulk_actions_response(self, request: HttpRequest) -> HttpResponse:
        """
        Returns the bulk actions response.
        """
        kind: Literal["modal", "action"] = request.POST.get("kind", "modal")
        name = request.POST.get("name", None)
        actions: dict[str, Action] = self.get_actions()

        if name is None or name not in actions:
            return HttpResponseServerError("Action not found")

        required_permissions = actions[name].permissions

        if not request.user.has_perms(required_permissions):
            return HttpResponseForbidden(
                "You don't have permission to perform this action"
            )

        qs = self.parse_ids(request)

        if kind == "modal":
            template_name = actions[name].template
            return render(
                request=request,
                template_name=template_name,
                context=self.get_modal_context_data(qs),
            )
        else:
            kwargs = {
                k: v
                for k, v in request.POST.items()
                if k in self.get_actions()[name].kwargs
            }
            return self.get_actions()[name].method(qs, **kwargs)

    def parse_ids(self, request: HttpRequest) -> QuerySet:
        """
        Parses the ids from the request.
        """
        ids = [int(id) for id in request.POST.getlist("action-check")]
        return self.get_queryset().filter(pk__in=ids)

    def get_export_response(self, request: HttpRequest) -> HttpResponse:
        """
        Returns the export response.
        """
        if (
            getattr(self.resource_class, "_serials") is None
            or "serial" not in self.resource_class.fields
        ):
            raise ValueError(
                "resource_class must have _serials attribute and serial field(SerialResourceMixin)",
            )

        app_label = self.get_app_label()
        verbose_name_plural = self.get_verbose_name_plural()
        object_name = self.get_object_name()

        required_perm = f"{app_label}.export_{object_name}"

        if not request.user.has_perm(required_perm):
            return HttpResponseForbidden(
                "You don't have permission to export this data"
            )

        content_types = {
            "csv": "text/csv",
            "json": "application/json",
            "xlsx": "application/vnd.ms-excel",
        }
        extension = request.GET.get("extension", "xlsx").lower()

        qs = self.get_queryset()
        self.resource_class._serials = []
        dataset: Dataset = self.resource_class().export(qs)

        now: str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        filename: str = f"{verbose_name_plural.title()}-{now}"

        dataset.title = verbose_name_plural.replace("_", " ").title()

        response = HttpResponse(
            getattr(dataset, extension),
            content_type=content_types[extension],
        )
        response["Content-Disposition"] = (
            f'attachment; filename="{filename}.{extension}"'
        )
        return response

    def get_model_class(self) -> type[Model]:
        """
        Returns the model class.
        """
        return self.model

    def get_template_name(self) -> str:
        """
        Returns the template name.
        Notes: you can use the *template_name* attribute to override the default template name.
        """
        if self.template_name:
            return self.template_name

        verbose_name_plural = self.get_verbose_name_plural()
        app_label = self.get_app_label()

        return f"apps/{app_label}/{verbose_name_plural}/index.html"

    def get_table_template_name(self) -> str:
        """
        Returns the table template name.
        Notes: you can use the table_template_name attribute to override the default table template name.
        """
        if self.table_template_name:
            return self.table_template_name

        verbose_name_plural = self.get_verbose_name_plural()
        app_label = self.get_app_label()

        return f"components/{app_label}/{verbose_name_plural}/table.html"

    def get_filter_form_template_name(self) -> str:
        """
        Returns the filter form template name.
        Notes: you can use the filter_form_template_name attribute to override the default filter form template name.
        """
        if self.filter_form_template_name:
            return self.filter_form_template_name

        verbose_name_plural = self.get_verbose_name_plural()
        app_label = self.get_app_label()

        return f"components/{app_label}/{verbose_name_plural}/filter-form.html"

    def get_queryset(self) -> QuerySet:
        """
        Returns the queryset.
        """
        if self.queryset is None:
            model = self.get_model_class()
            default_ordering = model._meta.ordering
            queryset = model.objects.all().order_by(*default_ordering)
        else:
            queryset = self.queryset

        request: HttpRequest = self.request

        OrderingFilter = self.get_ordering_filter_class()
        ordering_filter = OrderingFilter(request.GET, queryset)
        queryset = ordering_filter.qs

        SearchFilter = self.get_search_filter_class()
        search_filter = SearchFilter(request.GET, queryset)
        queryset = search_filter.qs

        filter_obj = self.filter_class(request.GET, queryset)
        queryset = filter_obj.qs

        return queryset

    def get_model_name(self) -> str:
        """
        return model name
        """
        return self.get_model_class()._meta.model_name

    def get_app_label(self) -> str:
        """
        Returns the app label using the model
        """
        return self.get_model_class()._meta.app_label

    def get_verbose_name_plural(self) -> str:
        """
        Returns the verbose name plural using the model.
        """
        model = self.get_model_class()
        return model._meta.codename_plural

    def get_object_name(self) -> str:
        """
        Returns the app label for single object using the model.
        """
        model = self.get_model_class()
        return model._meta.object_name.lower()

    def get_modal_context_data(self, qs: QuerySet, **kwargs) -> dict[str, Any]:
        """
        Returns the modal context data that will be passed to the template.
        """
        app_label = self.get_app_label()
        verbose_name_plural = self.get_verbose_name_plural()

        return {
            "qs": qs,
            **self.get_app_urls(app_label, verbose_name_plural),
            **self.get_html_ids(verbose_name_plural),
        }

    def filter_context_data(self, **kwargs) -> dict[str, Any]:
        """
        Returns the filter context data that will be passed to the template.
        """
        filter_obj = self.filter_class(self.request.GET, self.get_queryset())

        app_label = self.get_app_label()
        verbose_name_plural = self.get_verbose_name_plural()

        return {
            "filter": filter_obj,
            **self.get_app_urls(app_label, verbose_name_plural),
            **self.get_html_ids(verbose_name_plural),
        }

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """
        Returns the context data that will be passed to the template.
        """
        queryset = self.get_queryset()
        request: HttpRequest = self.request

        OrderingFilter = self.get_ordering_filter_class()
        ordering_filter = OrderingFilter(request.GET or request.POST, queryset.all())

        SearchFilter = self.get_search_filter_class()
        search_filter = SearchFilter(request.GET or request.POST, queryset.all())

        page = self.get_page_class(request=request, queryset=queryset)

        app_label = self.get_app_label()
        verbose_name_plural = self.get_verbose_name_plural()
        object_name = self.get_object_name()

        return {
            "page": page,
            "ordering_filter": ordering_filter,
            "search_filter": search_filter,
            "app_label": self.get_app_label(),
            "subapp_label": self.get_verbose_name_plural(),
            "model_name": self.get_model_name(),
            "model": self.get_model_class(),
            **self.get_app_urls(app_label, verbose_name_plural),
            **self.get_html_ids(verbose_name_plural),
            **self.get_permissions(request, app_label, object_name),
        }
