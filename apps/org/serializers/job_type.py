from rest_framework import serializers

from .. import models


class JobTypeSerializer(serializers.ModelSerializer):
    class JobSubtypeSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.JobSubtype
            fields = ("id", "name", "description")

    job_subtypes = JobSubtypeSerializer(many=True, read_only=True)
    job_subtypes_count = serializers.IntegerField(read_only=True)
    employees_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.JobType
        fields = (
            "id",
            "name",
            "description",
            "job_subtypes",
            "job_subtypes_count",
            "employees_count",
        )
