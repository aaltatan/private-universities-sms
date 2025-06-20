import json

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, View
from django.views.generic.list import MultipleObjectMixin
from django_filters import rest_framework as django_filters
from rest_framework import filters as rest_filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.core import filter_backends, mixins
from apps.core.inline import InlineFormsetFactory
from apps.core.utils import Deleter
from apps.core.schemas import Action

from .. import filters, forms, models, resources, serializers
from ..constants import vouchers as constants
from ..utils import VoucherAuditor, VoucherDeleter


class APIViewSet(
    mixins.APIMixin,
    mixins.BulkDeleteAPIMixin,
    viewsets.ModelViewSet,
):
    queryset = models.Voucher.objects.all().order_by("voucher_serial")
    serializer_class = serializers.VoucherSerializer
    filter_backends = [
        filter_backends.DjangoQLSearchFilter,
        django_filters.DjangoFilterBackend,
        rest_filters.OrderingFilter,
    ]
    filterset_class = filters.APIVoucherFilter
    ordering_fields = constants.ORDERING_FIELDS
    search_fields = constants.SEARCH_FIELDS
    deleter = VoucherDeleter

    @action(detail=True, methods=["post"], url_path="audit")
    def audit(self, request: Request, pk: int):
        instance = self.get_object()
        auditor = VoucherAuditor(request=request, obj=instance)
        auditor.action()

        if auditor.has_executed:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                {"details": auditor.get_message()},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=["post"], url_path="bulk-audit")
    def bulk_audit(self, request: Request):
        ids = request.data.get("ids", [])
        qs: QuerySet = self.queryset.filter(pk__in=ids)

        if not qs.exists():
            return Response(
                {"details": _("no objects found")},
                status=status.HTTP_404_NOT_FOUND,
            )

        auditor = VoucherAuditor(request=self.request, queryset=qs)
        auditor.action()

        if auditor.has_executed:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                {"details": auditor.get_message()},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ListView(
    PermissionRequiredMixin,
    mixins.BulkDeleteMixin,
    mixins.ListMixin,
    MultipleObjectMixin,
    View,
):
    permission_required = "trans.view_voucher"
    model = models.Voucher
    filter_class = filters.VoucherFilter
    resource_class = resources.VoucherResource
    deleter = VoucherDeleter
    ordering_fields = constants.ORDERING_FIELDS

    def bulk_audit(self, qs: QuerySet, **kwargs):
        response = HttpResponse()

        auditor = VoucherAuditor(request=self.request, queryset=qs)
        auditor.action()
        message = auditor.get_message()

        if auditor.has_executed:
            response["Hx-Location"] = json.dumps(
                {
                    "path": self.request.get_full_path(),
                    "target": f"#{self.get_html_ids()['table_id']}",
                }
            )
            messages.success(self.request, message)
        else:
            response["Hx-Retarget"] = "#no-content"
            response["HX-Reswap"] = "innerHTML"
            messages.error(self.request, message)

        response["HX-Trigger"] = "messages"
        return response

    def get_actions(self) -> dict[str, Action]:
        return {
            "delete": Action(
                method=self.bulk_delete,
                template="components/blocks/modals/bulk-delete.html",
                kwargs=("new_value",),
                permissions=("trans.delete_voucher",),
            ),
            "audit": Action(
                method=self.bulk_audit,
                template="components/trans/vouchers/modals/bulk-audit.html",
                permissions=("trans.audit_voucher",),
            ),
        }


class DetailsView(PermissionRequiredMixin, mixins.DetailsMixin, DetailView):
    permission_required = "trans.view_voucher"
    model = models.Voucher


class CreateView(PermissionRequiredMixin, mixins.CreateMixin, View):
    permission_required = "trans.add_voucher"
    form_class = forms.VoucherForm

    def perform_create(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.updated_by = self.request.user
        obj.save()
        return obj


class VoucherTransactionInline(InlineFormsetFactory):
    model = models.VoucherTransaction
    form_class = forms.VoucherTransactionForm
    fields = ("employee", "compensation", "quantity", "value", "notes")
    deleter = Deleter

    @classmethod
    def get_queryset(cls, obj: models.VoucherTransaction):
        return obj.transactions.all().order_by("ordering", "id")


class UpdateView(PermissionRequiredMixin, mixins.UpdateMixin, View):
    permission_required = "trans.change_voucher"
    form_class = forms.VoucherForm
    inlines = (VoucherTransactionInline,)

    def perform_update(self, form, formsets):
        obj = form.save(commit=False)
        for formset in formsets:
            last_order = 1
            for form in formset.forms:
                if form.is_valid() and form.cleaned_data:
                    item = form.save(commit=False)
                    item.ordering = form.cleaned_data.get("ORDER") or last_order
                    item.save()
                    last_order += 1
            formset.save()

        obj.updated_by = self.request.user
        obj.save()

        return obj


class DeleteView(PermissionRequiredMixin, mixins.BehaviorMixin, View):
    permission_required = "trans.delete_voucher"
    behavior = VoucherDeleter
    model = models.Voucher


class AuditView(PermissionRequiredMixin, mixins.BehaviorMixin, View):
    permission_required = "trans.audit_voucher"
    behavior = VoucherAuditor
    model = models.Voucher
    modal_template_name = "components/trans/vouchers/modals/audit.html"
