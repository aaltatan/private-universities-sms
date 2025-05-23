from rest_framework import serializers

from .. import models


class PeriodSerializer(serializers.ModelSerializer):
    class YearSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.Year
            fields = ("id", "name", "description")

    year = YearSerializer(read_only=True)
    is_closed = serializers.BooleanField(required=False)

    class Meta:
        model = models.Period
        fields = (
            "id",
            "name",
            "year",
            "start_date",
            "is_closed",
            "description",
        )


class CreateUpdatePeriodSerializer(serializers.ModelSerializer):
    year = serializers.PrimaryKeyRelatedField(
        queryset=models.Year.objects.all(),
    )

    class Meta:
        model = models.Period
        fields = (
            "name",
            "year",
            "start_date",
            "is_closed",
            "description",
        )
