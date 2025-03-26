from django_filters import rest_framework as django_filters
from rest_framework import filters as rest_filters
from rest_framework import viewsets

from apps.core import filter_backends, mixins
from apps.core.utils import Deleter

from .. import filters, models, serializers


class APIViewSet(
    mixins.APIMixin,
    mixins.BulkDeleteAPIMixin,
    viewsets.ModelViewSet,
):
    queryset = models.Mobile.objects.all()
    serializer_class = serializers.MobileSerializer
    filter_backends = [
        filter_backends.DjangoQLSearchFilter,
        django_filters.DjangoFilterBackend,
        rest_filters.OrderingFilter,
    ]
    filterset_class = filters.APIMobileFilter
    ordering_fields = ("id", "number")
    search_fields = (
        "number",
        "employee__firstname",
        "employee__father_name",
        "employee__lastname",
        "employee__national_id",
    )
    deleter = Deleter

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return serializers.MobileCreateSerializer
        return serializers.MobileSerializer
