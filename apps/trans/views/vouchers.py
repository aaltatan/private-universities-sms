import json

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import QuerySet
from django.contrib import messages
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, View
from django.views.generic.list import MultipleObjectMixin
from django_filters import rest_framework as django_filters
from rest_framework import filters as rest_filters
from rest_framework import viewsets

from apps.core import filter_backends, mixins

# from apps.core.inline import InlineFormsetFactory
from apps.core.schemas import Action
from apps.core.utils import Deleter

from .. import filters, forms, models, resources, serializers
from ..constants import vouchers as constants


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
    deleter = Deleter


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
    deleter = Deleter
    ordering_fields = constants.ORDERING_FIELDS

    def bulk_audit(self, qs: QuerySet, **kwargs):
        response = HttpResponse()

        if not qs.filter(updated_by=self.request.user).exists():
            response["Hx-Location"] = json.dumps(
                {
                    "path": self.request.get_full_path(),
                    "target": f"#{self.get_html_ids()['table_id']}",
                }
            )
            qs.update(is_audited=True, audited_by=self.request.user)
            message = _("vouchers audited successfully").title()
            messages.success(self.request, message)
        else:
            response["Hx-Retarget"] = "#no-content"
            response["HX-Reswap"] = "innerHTML"
            message = _(
                "you can't audit your the vouchers that you have created or updated"
            ).title()
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


# class VoucherTransactionInline(InlineFormsetFactory):
#     model = models.VoucherTransaction
#     form_class = forms.VoucherTransactionForm
#     fields = ("name", "kind", "description")

#     @classmethod
#     def get_queryset(cls, obj: models.Voucher):
#         return obj.transactions.all().order_by("ordering", "id")


class UpdateView(PermissionRequiredMixin, mixins.UpdateMixin, View):
    permission_required = "trans.change_voucher"
    form_class = forms.VoucherForm
    # inlines = (VoucherTransactionInline,)


class DeleteView(PermissionRequiredMixin, mixins.DeleteMixin, View):
    permission_required = "trans.delete_voucher"
    deleter = Deleter
    model = models.Voucher
