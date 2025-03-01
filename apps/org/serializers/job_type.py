from rest_framework import serializers

from .. import models


class JobTypeSerializer(serializers.ModelSerializer):
    class JobSubtypeSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.JobSubtype
            fields = ("id", "name", "description")

    job_subtypes = JobSubtypeSerializer(many=True, read_only=True)
    job_subtypes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.JobType
        fields = (
            "id",
            "name",
            "description",
            "job_subtypes",
            "job_subtypes_count",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["job_subtypes"] = {
            "count": representation.pop("job_subtypes_count"),
            "results": representation.pop("job_subtypes"),
        }
        return representation


class JobTypeActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.JobType
        fields = ("name", "description")
