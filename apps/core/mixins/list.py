from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Literal

from django.core.paginator import EmptyPage, Page, PageNotAnInteger, Paginator
from django.db.models import Model, QuerySet
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseServerError,
)
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from django_filters import FilterSet
from import_export.resources import ModelResource
from rest_framework.serializers import ModelSerializer
from tablib import Dataset

from ..constants import PERMISSION
from ..schemas import Action


class ListMixin(ABC):
    """
    A mixin that adds a list view.
    """

    @property
    @abstractmethod
    def filter_class(self) -> type[FilterSet]:
        pass

    @property
    @abstractmethod
    def activity_serializer(self) -> type[ModelSerializer]:
        pass

    @property
    @abstractmethod
    def resource_class(self) -> type[ModelResource]:
        pass

    @abstractmethod
    def get_actions(self) -> dict[str, Action]:
        pass

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Handles GET requests and returns a rendered template.
        """
        if request.GET.get("redirected"):
            return self.get_export_response(request)

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
        filename: str = f"{self.get_verbose_name_plural().title()}-{now}"

        dataset.title = filename

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
        if getattr(self, "model", None):
            return self.model

        return self.filter_class.Meta.model

    def get_template_name(self) -> str:
        """
        Returns the template name.
        Notes: you can use the *template_name* attribute to override the default template name.
        """
        if getattr(self, "template_name", None):
            return self.template_name

        verbose_name_plural: str = self.get_verbose_name_plural()

        return f"apps/{verbose_name_plural}/index.html"

    def get_table_template_name(self) -> str:
        """
        Returns the table template name.
        Notes: you can use the table_template_name attribute to override the default table template name.
        """
        verbose_name_plural = self.get_verbose_name_plural()

        if getattr(self, "table_template_name", None):
            return self.table_template_name

        return f"components/{verbose_name_plural}/table.html"

    def get_queryset(self) -> QuerySet:
        """
        Returns the queryset.
        """
        model = self.get_model_class()
        qs = model.objects.all().order_by("id")

        request: HttpRequest = self.request

        filter_class = self.filter_class(request.GET, qs)

        qs = filter_class.qs

        return qs

    def get_permissions(self) -> dict[str, bool]:
        """
        Returns a dictionary of permissions.
        """
        return {
            "can_view": self.get_permission("view"),
            "can_create": self.get_permission("add"),
            "can_update": self.get_permission("change"),
            "can_delete": self.get_permission("delete"),
            "can_export": self.get_permission("export"),
            "can_view_activity": self.get_permission("view_activity"),
        }

    def get_permission(self, permission: PERMISSION) -> bool:
        """
        Returns whether the user has a given permission.
        """
        app_label = self.get_app_label()
        object_name: str = self.get_object_name()
        permission_string: str = f"{app_label}.{permission}_{object_name}"

        request: HttpRequest = self.request

        return request.user.has_perm(permission_string)

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
        return model._meta.verbose_name_plural

    def get_object_name(self) -> str:
        """
        Returns the app label for single object using the model.
        """
        model = self.get_model_class()
        return model._meta.object_name.lower()

    def get_per_page(self) -> int:
        """
        Returns the number of items to show per page.
        """
        request: HttpRequest = self.request

        default_per_page: int = settings.PER_PAGE
        request_per_page: str = request.GET.get("per_page", None)

        if request_per_page == "all":
            return settings.MAX_PAGE_SIZE

        return request_per_page or default_per_page

    def get_page_class(self) -> Page:
        """
        Returns the page class.
        """
        request: HttpRequest = self.request
        qs = self.get_queryset()

        per_page: int = self.get_per_page()

        paginator: Paginator = Paginator(qs, per_page)
        page: int = request.GET.get("page", 1)

        try:
            page = paginator.page(page)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        return page

    def get_app_urls(self) -> dict[str, str]:
        """
        Returns the app links.
        """
        verbose_name_plural: str = self.get_verbose_name_plural()
        return {
            "index_url": reverse(f"{verbose_name_plural}:index"),
            "create_url": reverse(f"{verbose_name_plural}:create"),
        }

    def get_html_ids(self) -> dict[str, str]:
        """
        Returns the html ids.
        """
        verbose_name_plural: str = self.get_verbose_name_plural()
        return {
            "table_id": f"{verbose_name_plural}-table",
            "form_table_id": f"{verbose_name_plural}-form-table",
            "filter_form_id": f"{verbose_name_plural}-filter",
        }

    def get_modal_context_data(self, qs: QuerySet, **kwargs) -> dict[str, Any]:
        """
        Returns the modal context data that will be passed to the template.
        """
        return {
            "qs": qs,
            **self.get_app_urls(),
            **self.get_html_ids(),
        }

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """
        Returns the context data that will be passed to the template.
        """
        qs: QuerySet = self.get_queryset()
        request: HttpRequest = self.request
        filter_class = self.filter_class(request.GET or request.POST, qs.all())
        page: Page = self.get_page_class()

        page.paginator.count

        return {
            "page": page,
            "filter": filter_class,
            "app_label": self.get_app_label(),
            "subapp_label": self.get_verbose_name_plural(),
            "model_name": self.get_model_name(),
            **self.get_app_urls(),
            **self.get_html_ids(),
            **self.get_permissions(),
        }
