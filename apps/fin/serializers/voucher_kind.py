from rest_framework import serializers

from .. import models


class VoucherKindSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VoucherKind
        fields = ("id", "name", "description")
