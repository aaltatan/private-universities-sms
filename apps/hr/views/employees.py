from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView, View
from django.views.generic.list import MultipleObjectMixin
# from django_filters import rest_framework as django_filters
# from rest_framework import filters as rest_filters
# from rest_framework import viewsets

from apps.core import mixins
from apps.core.schemas import Action
from apps.core.utils import Deleter
from apps.core.inline import InlineFormsetFactory

from .. import filters, forms, models, resources  # , serializers
from ..constants import employee as constants


# class APIViewSet(
#     mixins.APIMixin,
#     mixins.BulkDeleteAPIMixin,
#     viewsets.ModelViewSet,
# ):
#     queryset = models.Employee.objects.all()
#     serializer_class = serializers.EmployeeSerializer
#     filter_backends = [
#         filter_backends.DjangoQLSearchFilter,
#         django_filters.DjangoFilterBackend,
#         rest_filters.OrderingFilter,
#     ]
#     filterset_class = filters.APIEmployeeFilter
#     ordering_fields = constants.ORDERING_FIELDS
#     search_fields = constants.SEARCH_FIELDS
#     deleter = Deleter


class ListView(
    PermissionRequiredMixin,
    mixins.BulkDeleteMixin,
    mixins.ListMixin,
    MultipleObjectMixin,
    View,
):
    permission_required = "hr.view_employee"
    model = models.Employee
    filter_class = filters.EmployeeFilter
    resource_class = resources.EmployeeResource
    deleter = Deleter
    ordering_fields = constants.ORDERING_FIELDS

    def get_actions(self) -> dict[str, Action]:
        return {
            "delete": Action(
                method=self.bulk_delete,
                template="components/blocks/modals/bulk-delete.html",
                kwargs=("new_value",),
                permissions=("hr.delete_employee",),
            ),
        }


class DetailsView(PermissionRequiredMixin, mixins.DetailsMixin, DetailView):
    permission_required = "hr.view_employee"
    model = models.Employee


class CreateView(PermissionRequiredMixin, mixins.CreateMixin, View):
    permission_required = "hr.add_employee"
    form_class = forms.EmployeeForm


class MobileInline(InlineFormsetFactory):
    model = models.Mobile
    form_class = forms.MobileForm
    fields = ("number", "has_whatsapp", "kind", "notes")

    @classmethod
    def get_queryset(cls, obj: models.Employee):
        return obj.mobiles.all().order_by("id")


class PhoneInline(InlineFormsetFactory):
    model = models.Phone
    form_class = forms.PhoneForm
    fields = ("number", "kind", "notes")

    @classmethod
    def get_queryset(cls, obj: models.Employee):
        return obj.phones.all().order_by("id")


class EmailInline(InlineFormsetFactory):
    model = models.Email
    form_class = forms.EmailForm
    fields = ("email", "kind", "notes")

    @classmethod
    def get_queryset(cls, obj: models.Employee):
        return obj.emails.all().order_by("id")


class UpdateView(PermissionRequiredMixin, mixins.UpdateMixin, View):
    permission_required = "hr.change_employee"
    form_class = forms.EmployeeForm
    inlines = (MobileInline, PhoneInline, EmailInline)


class DeleteView(PermissionRequiredMixin, mixins.DeleteMixin, View):
    permission_required = "hr.delete_employee"
    deleter = Deleter
    model = models.Employee
