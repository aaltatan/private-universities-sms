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
    queryset = models.Email.objects.all()
    serializer_class = serializers.EmailSerializer
    filter_backends = [
        filter_backends.DjangoQLSearchFilter,
        django_filters.DjangoFilterBackend,
        rest_filters.OrderingFilter,
    ]
    filterset_class = filters.APIEmailFilter
    ordering_fields = ("id", "email")
    search_fields = (
        "number",
        "employee__firstname",
        "employee__father_name",
        "employee__lastname",
        "employee__national_id",
    )
    deleter = Deleter
