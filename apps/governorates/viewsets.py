from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.core.filter_backends import DjangoQLSearchFilter

from . import constants, models, serializers


class GovernorateViewSet(viewsets.ModelViewSet):
    queryset = models.Governorate.objects.all()
    serializer_class = serializers.GovernorateSerializer
    filter_backends = [
        DjangoQLSearchFilter,
        filters.OrderingFilter,
    ]
    ordering_fields = constants.ORDERING_FIELDS
    search_fields = constants.SEARCH_FIELDS

    @action(detail=False, methods=["post"], url_path="bulk-delete")
    def bulk_delete(self, request: Request):
        """
        Deletes the selected objects.
        """
        ids = request.data.get("ids", [])
        return Response(
            {"hello": "world"},
            status=200,
        )
