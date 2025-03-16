from rest_framework import serializers

from .. import models


class JobSubtypeSerializer(serializers.ModelSerializer):
    class JobTypeSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.JobSubtype
            fields = ("id", "name", "description")

    job_type = JobTypeSerializer()
    employees_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.JobSubtype
        fields = (
            "id",
            "name",
            "description",
            "job_type",
            "employees_count",
        )


class CreateUpdateJobSubtypeSerializer(serializers.ModelSerializer):
    job_type = serializers.PrimaryKeyRelatedField(
        queryset=models.JobType.objects.all(),
    )

    class Meta:
        model = models.JobSubtype
        fields = ("name", "job_type", "description")
