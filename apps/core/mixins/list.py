import json
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Literal

import django_filters as filters
from django.contrib import messages
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

from apps.core.utils.behaviors import ActionBehavior

from ..constants import PERMISSION
from ..filters import BaseQSearchFilter, get_ordering_filter
from ..forms import BehaviorForm
from ..models import GlobalSetting
from ..schemas import Action


class SidebarFilterMixin(ABC):
    """
    this class will not work except if combined with TemplateVariablesMixin.
    """

    @property
    @abstractmethod
    def filter_class(self) -> type[FilterSet]:
        pass

    @abstractmethod
    def get_index_url(self) -> dict[str, str]:
        pass

    @abstractmethod
    def get_html_ids(self) -> dict[str, str]:
        pass

    def get_filters_response(
        self,
        request: HttpRequest,
        template_name: str,
        context: dict[str, Any],
    ) -> HttpResponse:
        """
        Returns the filters response.
        """
        response = render(request, template_name, context)
        response["Hx-Trigger"] = "open-overlay-sidebar"
        return response

    def sidebar_filters_context_data(
        self, request: HttpRequest, queryset: QuerySet, **kwargs
    ) -> dict[str, Any]:
        """
        Returns the filter context data that will be passed to the template.
        """
        filter_obj = self.filter_class(request.GET, queryset, request=request)

        return {
            "filter": filter_obj,
            "index_url": self.get_index_url(),
            **self.get_html_ids(),
        }


class ObjectNamesMixin:
    model: type[Model] | None = None
    app_label: str | None = None
    codename_plural: str | None = None
    object_name: str | None = None
    model_name: str | None = None

    def get_model_name(self) -> str:
        """
        return model name
        """
        if getattr(self, "model_name", None):
            return self.model_name

        return self.model._meta.model_name

    def get_app_label(self) -> str:
        """
        Returns the app label using the model
        """
        if getattr(self, "app_label", None):
            return self.app_label

        return self.model._meta.app_label

    def get_codename_plural(self) -> str:
        """
        Returns the codename plural using the model.
        """
        if getattr(self, "codename_plural", None):
            return self.codename_plural

        return self.model._meta.codename_plural

    def get_object_name(self) -> str:
        """
        Returns the app label for single object using the model.
        """
        if getattr(self, "object_name", None):
            return self.object_name

        return self.model._meta.object_name.lower()


class TemplateNamesMixin(ObjectNamesMixin):
    template_name: str | None = None
    table_template_name: str | None = None
    filter_form_template_name: str | None = None

    def get_template_name(self) -> str:
        """
        Returns the template name.
        Notes: you can use the *template_name* attribute to override the default template name.
        """
        if self.template_name:
            return self.template_name

        codename_plural = self.get_codename_plural()
        app_label = self.get_app_label()

        return f"apps/{app_label}/{codename_plural}/index.html"

    def get_table_template_name(self) -> str:
        """
        Returns the table template name.
        Notes: you can use the table_template_name attribute to override the default table template name.
        """
        if self.table_template_name:
            return self.table_template_name

        codename_plural = self.get_codename_plural()
        app_label = self.get_app_label()

        return f"components/{app_label}/{codename_plural}/table.html"

    def get_filter_form_template_name(self) -> str:
        """
        Returns the filter form template name.
        Notes: you can use the filter_form_template_name attribute to override the default filter form template name.
        """
        if self.filter_form_template_name:
            return self.filter_form_template_name

        codename_plural = self.get_codename_plural()
        app_label = self.get_app_label()

        return f"components/{app_label}/{codename_plural}/filter-form.html"


class TemplateVariablesMixin(ObjectNamesMixin):
    def get_html_ids(self) -> dict[str, str]:
        """
        Returns the html ids.
        """
        codename_plural = self.get_codename_plural()
        return {
            "table_id": f"{codename_plural}-table",
            "form_table_id": f"{codename_plural}-form-table",
            "filter_form_id": f"{codename_plural}-filter",
        }

    def get_index_url(self) -> str:
        """
        Returns index urls.
        """
        app_label = self.get_app_label()
        codename_plural = self.get_codename_plural()

        return reverse(f"{app_label}:{codename_plural}:index")

    def get_create_url(self) -> str | None:
        """
        Returns add url.
        """
        app_label = self.get_app_label()
        codename_plural = self.get_codename_plural()

        # in case of no create view
        try:
            create_url = reverse(f"{app_label}:{codename_plural}:create")
        except NoReverseMatch:
            create_url = None

        return create_url

    def get_permissions(self, request: HttpRequest) -> dict[str, bool]:
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
            f"can_{permission}": self._get_perm(request, permission)
            for permission in permissions
        }

    def _get_perm(self, request: HttpRequest, permission: PERMISSION) -> bool:
        """
        Returns whether the user has a given permission.
        """
        app_label = self.get_app_label()
        object_name = self.get_object_name()

        permission_string = f"{app_label}.{permission}_{object_name}"

        return request.user.has_perm(permission_string)


class SearchFilterMixin(ABC):
    search_filter: bool = True
    search_filter_class: type[FilterSet] | None = None

    @property
    @abstractmethod
    def model(self) -> type[Model]:
        pass

    def get_search_filter_class(self) -> type[FilterSet]:
        """
        Returns the search filter class.
        """
        if getattr(self, "search_filter_class", None):
            return self.search_filter_class

        class SearchFilter(BaseQSearchFilter):
            class Meta:
                model = self.model
                fields = ("id",)

        return SearchFilter


class OrderFilterMixin(ABC):
    order_filter: bool = True
    ordering_filter_class: type[FilterSet] | None = None

    @property
    @abstractmethod
    def model(self) -> type[Model]:
        pass

    def get_ordering_filter_class(self) -> type[FilterSet]:
        """
        Returns the ordering filter class.
        """
        if getattr(self, "ordering_fields", None) is None:
            raise AttributeError(
                "you must define the ordering_fields attribute.",
            )
        if getattr(self, "ordering_filter_class", None):
            return self.ordering_filter_class

        class OrderingFilter(filters.FilterSet):
            ordering = get_ordering_filter(self.ordering_fields)

            class Meta:
                model = self.model
                fields = ("id",)

        return OrderingFilter


class PaginationMixin:
    def _get_per_page(self, request: HttpRequest) -> int:
        """
        Returns the number of items to show per page.
        """
        global_setting = GlobalSetting.get_solo()

        default_per_page: int = global_setting.per_page
        request_per_page: str = request.GET.get("per_page", None)

        if request_per_page == "all":
            return global_setting.max_page_size

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


class ListMixin(
    TemplateVariablesMixin,
    PaginationMixin,
    SearchFilterMixin,
    OrderFilterMixin,
    SidebarFilterMixin,
    TemplateNamesMixin,
    ABC,
):
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

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Handles GET requests and returns a rendered template.
        """
        if request.GET.get("redirected"):
            return self.get_export_response(request)

        if request.GET.get("filters"):
            template_name = self.get_filter_form_template_name()

            queryset = self.get_queryset()
            queryset = self.get_filtered_queryset(request, queryset)

            context = self.sidebar_filters_context_data(
                request=request, queryset=queryset
            )

            return self.get_filters_response(request, template_name, context)

        template_name = self.get_template_name()

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

    def get_actions(self) -> dict[str, Action]:
        """
        Returns the actions.
        """
        pass

    def get_bulk_actions_response(self, request: HttpRequest) -> HttpResponse:
        """
        Returns the bulk actions response.
        """
        if getattr(self, "get_actions", None) is None:
            raise AttributeError(
                "you must define the get_actions method",
            )
        else:
            actions = self.get_actions()
            if not isinstance(actions, dict):
                raise TypeError(
                    "the get_actions method must return a dictionary of Actions",
                )

        kind: Literal["modal", "action"] = request.POST.get("kind", "modal")
        action_name = request.POST.get("name", None)
        actions: dict[str, Action] = self.get_actions()

        if action_name is None or action_name not in actions:
            return HttpResponseServerError("Action not found")

        required_permissions = actions[action_name].permissions

        if not request.user.has_perms(required_permissions):
            return HttpResponseForbidden(
                "You don't have permission to perform this action"
            )

        qs = self.get_queryset_pks(request)

        if kind == "modal":
            kwargs = {"qs": qs}
            if actions[action_name].form_class is not None:
                kwargs["form"] = actions[action_name].form_class()
            response = render(
                request=request,
                template_name=actions[action_name].template,
                context=self.get_bulk_context_data(**kwargs),
            )
            response["HX-Trigger"] = "showmodal"
            return response
        else:
            behavior = self.get_actions()[action_name].behavior(request, queryset=qs)
            if actions[action_name].form_class is None:
                return self.get_behavior_action_response(request, behavior)
            else:
                form = actions[action_name].form_class(request.POST)
                if form.is_valid():
                    return self.get_behavior_action_response(request, behavior, form)
                else:
                    return render(
                        request=request,
                        template_name=actions[action_name].template,
                        context=self.get_bulk_context_data(qs, form=form),
                    )

    def get_success_bulk_response(self, request: HttpRequest, message: str):
        response = HttpResponse()
        response["Hx-Location"] = json.dumps(
            {
                "path": request.get_full_path(),
                "target": f"#{self.get_html_ids()['table_id']}",
            }
        )
        messages.success(request, message)
        response["HX-Trigger"] = "messages, hidemodal"
        return response

    def get_error_bulk_response(self, request: HttpRequest, message: str):
        response = HttpResponse()
        response["Hx-Retarget"] = "#no-content"
        response["HX-Reswap"] = "innerHTML"
        response["HX-Trigger"] = "messages, hidemodal"
        messages.error(request, message)
        return response

    def get_behavior_action_response(
        self,
        request: HttpRequest,
        behavior: ActionBehavior,
        form: BehaviorForm | None = None,
    ) -> HttpResponse:
        """
        Performs the action.
        """
        behavior.action()
        message = behavior.get_message()
        if behavior.has_executed:
            if form is not None:
                form.save()
            return self.get_success_bulk_response(request, message)
        else:
            return self.get_error_bulk_response(request, message)

    def get_queryset_pks(self, request: HttpRequest) -> QuerySet:
        """
        Parses the ids from the request.
        """
        ids = [int(id) for id in request.POST.getlist("action_check")]

        queryset = self.get_queryset()
        queryset = self.get_filtered_queryset(request, queryset)

        return queryset.filter(pk__in=ids)

    def get_bulk_context_data(self, qs: QuerySet, **kwargs) -> dict[str, Any]:
        """
        Returns the modal context data that will be passed to the template.
        """
        return {
            "qs": qs,
            "create_url": self.get_create_url(),
            "index_url": self.get_index_url(),
            **self.get_html_ids(),
            **kwargs,
        }

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

        queryset = self.get_queryset()
        queryset = self.get_filtered_queryset(request, queryset)

        self.resource_class._serials = []
        dataset: Dataset = self.resource_class().export(queryset)

        filename = self.get_filename()
        dataset.title = self.get_dataset_title()

        response = HttpResponse(
            getattr(dataset, extension),
            content_type=content_types[extension],
        )
        response["Content-Disposition"] = (
            f'attachment; filename="{filename}.{extension}"'
        )
        return response

    def get_dataset_title(self) -> str:
        """
        Returns the dataset title.
        """
        return self.get_codename_plural().replace("_", " ").title()

    def get_filename(self) -> str:
        """
        Returns the filename.
        """
        codename_plural = self.get_codename_plural()
        now: str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        return f"{codename_plural.title()}-{now}"

    def get_filtered_queryset(
        self, request: HttpRequest, queryset: QuerySet
    ) -> QuerySet:
        """
        Returns the filtered queryset.
        Steps:
        1. Filter the queryset by ordering filter
        2. Filter the queryset by search filter
        3. Filter the queryset by filter class (sidebar)
        """
        ordered_by = queryset.query.order_by

        # Step 1: Filter the queryset by ordering filter
        if self.order_filter:
            OrderingFilter = self.get_ordering_filter_class()
            ordering_filter = OrderingFilter(request.GET, queryset, request=request)
            queryset = ordering_filter.qs

        if not request.GET.get("ordering"):
            if ordered_by:
                queryset = queryset.order_by(*ordered_by)
            else:
                default_ordering = self.model._meta.ordering
                queryset = queryset.order_by(*default_ordering)

        # Step 2: Filter the queryset by search filter
        if self.search_filter:
            SearchFilter = self.get_search_filter_class()
            search_filter = SearchFilter(request.GET, queryset, request=request)
            queryset = search_filter.qs

        # Step 3: Filter the queryset by filter class (sidebar)
        filter_obj = self.filter_class(request.GET, queryset, request=request)
        queryset = filter_obj.qs

        return queryset

    def get_queryset(self) -> QuerySet:
        """
        Returns the queryset.
        """
        return self.model.objects.all()

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """
        Returns the context data that will be passed to the template.
        """
        request: HttpRequest = self.request

        queryset = self.get_queryset()
        queryset = self.get_filtered_queryset(request, queryset)

        context = {
            "app_label": self.get_app_label(),
            "subapp_label": self.get_codename_plural(),
            "model_name": self.get_model_name(),
            "model": self.model,
            "create_url": self.get_create_url(),
            "index_url": self.get_index_url(),
            **self.get_html_ids(),
            **self.get_permissions(request),
            **kwargs,
        }

        if self.search_filter:
            SearchFilter = self.get_search_filter_class()
            search_filter = SearchFilter(
                request.GET or request.POST,
                queryset.all(),
                request=request,
            )
            context["search_filter"] = search_filter

        if self.order_filter:
            OrderingFilter = self.get_ordering_filter_class()
            ordering_filter = OrderingFilter(
                request.GET or request.POST,
                queryset.all(),
                request=request,
            )
            context["ordering_filter"] = ordering_filter

        context["filter"] = self.filter_class(
            request.GET or request.POST,
            queryset.all(),
            request=request,
        )

        page = self.get_page_class(request=request, queryset=queryset)
        context["page"] = page

        return context
