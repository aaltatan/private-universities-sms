from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import resolve
from django.utils import timezone
from django.views.generic import DetailView, View
from django_filters import rest_framework as django_filters
from rest_framework import filters as rest_filters
from rest_framework import parsers, viewsets

from apps.core import filter_backends, mixins
from apps.core.inline import InlineFormsetFactory
from apps.core.models import Template
from apps.core.schemas import Action
from apps.core.utils import Deleter

from .. import filters, forms, models, resources, serializers
from ..constants import employee as constants


class APIViewSet(
    mixins.APIMixin,
    mixins.BulkDeleteAPIMixin,
    viewsets.ModelViewSet,
):
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer
    filter_backends = [
        filter_backends.DjangoQLSearchFilter,
        django_filters.DjangoFilterBackend,
        rest_filters.OrderingFilter,
    ]
    filterset_class = filters.APIEmployeeFilter
    ordering_fields = constants.ORDERING_FIELDS
    search_fields = constants.SEARCH_FIELDS
    deleter = Deleter
    parser_classes = (
        parsers.JSONParser,
        parsers.MultiPartParser,
        parsers.FormParser,
    )

    def get_queryset(self):
        settings = models.HRSetting.get_solo()
        return (
            models.Employee.objects.select_related(
                # geo
                "city",
                "city__governorate",
                "nationality",
                # org
                "cost_center",
                "position",
                "status",
                "job_subtype",
                "job_subtype__job_type",
                # edu
                "degree",
                "school",
                "school__kind",
                "school__nationality",
                "specialization",
            )
            .prefetch_related("emails", "phones", "mobiles", "groups")
            .annotate_dates(
                settings.nth_job_anniversary,
                settings.years_count_to_group_job_age,
            )
        )

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return serializers.EmployeeCreateUpdateSerializer
        return serializers.EmployeeSerializer


class ListView(PermissionRequiredMixin, mixins.ListMixin, View):
    permission_required = "hr.view_employee"
    model = models.Employee
    filter_class = filters.EmployeeFilter
    resource_class = resources.EmployeeResource
    ordering_fields = constants.ORDERING_FIELDS

    def get_queryset(self):
        return models.Employee.objects.select_related(
            # geo
            "city",
            "city__governorate",
            # org
            "cost_center",
            "position",
            "status",
            "job_subtype",
            "job_subtype__job_type",
            # edu
            "degree",
            "specialization",
        ).prefetch_related("groups")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context

    def get_actions(self) -> dict[str, Action]:
        return {
            "delete": Action(
                behavior=Deleter,
                template="components/blocks/modals/bulk-delete.html",
                permissions=("hr.delete_employee",),
            ),
        }


class DetailsView(PermissionRequiredMixin, mixins.DetailsMixin, DetailView):
    permission_required = "hr.view_employee"
    model: models.Employee = models.Employee

    def get_queryset(self):
        settings = models.HRSetting.get_solo()
        return (
            self.model.objects.select_related(
                # geo
                "city",
                "city__governorate",
                "nationality",
                # org
                "cost_center",
                "position",
                "status",
                "job_subtype",
                "job_subtype__job_type",
                # edu
                "degree",
                "school",
                "school__kind",
                "school__nationality",
                "specialization",
            )
            .prefetch_related("emails", "phones", "mobiles", "groups")
            .annotate_dates(
                settings.nth_job_anniversary,
                settings.years_count_to_group_job_age,
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


class CreateView(PermissionRequiredMixin, mixins.CreateMixin, View):
    permission_required = "hr.add_employee"
    form_class = forms.EmployeeForm


class MobileInline(InlineFormsetFactory):
    model = models.Mobile
    form_class = forms.MobileForm
    fields = ("number", "has_whatsapp", "kind", "notes")
    deleter = Deleter

    @classmethod
    def get_queryset(cls, obj: models.Employee):
        return obj.mobiles.all().order_by("id")


class PhoneInline(InlineFormsetFactory):
    model = models.Phone
    form_class = forms.PhoneForm
    fields = ("number", "kind", "notes")
    deleter = Deleter

    @classmethod
    def get_queryset(cls, obj: models.Employee):
        return obj.phones.all().order_by("id")


class EmailInline(InlineFormsetFactory):
    model = models.Email
    form_class = forms.EmailForm
    fields = ("email", "kind", "notes")
    deleter = Deleter

    @classmethod
    def get_queryset(cls, obj: models.Employee):
        return obj.emails.all().order_by("id")


class UpdateView(PermissionRequiredMixin, mixins.UpdateMixin, View):
    permission_required = "hr.change_employee"
    form_class = forms.EmployeeForm
    inlines = (MobileInline, PhoneInline, EmailInline)


class DeleteView(PermissionRequiredMixin, mixins.BehaviorMixin, View):
    permission_required = "hr.delete_employee"
    behavior = Deleter
    model = models.Employee


class ExportToMSWordView(
    PermissionRequiredMixin,
    mixins.ExportToMSWordMixin,
    View,
):
    permission_required = "hr.export_employee"

    def get_template(self):
        return Template.get_employee_template()

    def get_filename(self):
        return "employee details"

    def get_context_data(self):
        resolved = resolve(self.request.path_info)
        return {
            "employee": models.Employee.objects.get(
                slug=resolved.kwargs.get("slug"),
            ),
        }
