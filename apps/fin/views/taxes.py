from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView, View
from django_filters import rest_framework as django_filters
from rest_framework import filters as rest_filters
from rest_framework import viewsets

from apps.core import filter_backends, mixins
from apps.core.inline import InlineFormsetFactory
from apps.core.schemas import Action
from apps.core.utils import Deleter

from .. import filters, forms, models, resources, serializers
from ..constants import taxes as constants


class APIViewSet(
    mixins.APIMixin,
    mixins.BulkDeleteAPIMixin,
    viewsets.ModelViewSet,
):
    queryset = (
        models.Tax.objects.annotate_compensations_count()
        .annotate_brackets_count()
        .all()
    )
    serializer_class = serializers.TaxSerializer
    filter_backends = [
        filter_backends.DjangoQLSearchFilter,
        django_filters.DjangoFilterBackend,
        rest_filters.OrderingFilter,
    ]
    filterset_class = filters.APITaxFilter
    ordering_fields = constants.ORDERING_FIELDS
    search_fields = constants.SEARCH_FIELDS
    deleter = Deleter


class ListView(PermissionRequiredMixin, mixins.ListMixin, View):
    permission_required = "fin.view_tax"
    model = models.Tax
    filter_class = filters.TaxFilter
    resource_class = resources.TaxResource
    ordering_fields = constants.ORDERING_FIELDS

    def get_queryset(self):
        return (
            models.Tax.objects.annotate_compensations_count()
            .annotate_brackets_count()
            .all()
        )

    def get_actions(self) -> dict[str, Action]:
        return {
            "delete": Action(
                behavior=Deleter,
                template="components/blocks/modals/bulk-delete.html",
                permissions=("fin.delete_tax",),
            ),
        }


class DetailsView(PermissionRequiredMixin, mixins.DetailsMixin, DetailView):
    permission_required = "fin.view_tax"
    model = models.Tax

    def get_queryset(self):
        return (
            models.Tax.objects.annotate_compensations_count()
            .annotate_brackets_count()
            .all()
        )


class CreateView(PermissionRequiredMixin, mixins.CreateMixin, View):
    permission_required = "fin.add_tax"
    form_class = forms.TaxForm


class TaxBracketInline(InlineFormsetFactory):
    model = models.TaxBracket
    form_class = forms.TaxBracketForm
    fields = ("amount_from", "amount_to", "rate", "notes")
    deleter = Deleter

    @classmethod
    def get_queryset(cls, obj: models.Tax):
        return obj.brackets.all().order_by("ordering", "id")


class UpdateView(PermissionRequiredMixin, mixins.UpdateMixin, View):
    permission_required = "fin.change_tax"
    form_class = forms.TaxForm
    inlines = (TaxBracketInline,)


class DeleteView(PermissionRequiredMixin, mixins.BehaviorMixin, View):
    permission_required = "fin.delete_tax"
    behavior = Deleter
    model = models.Tax
