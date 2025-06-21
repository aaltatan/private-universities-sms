from rest_framework import serializers

from .. import models


class EmailSerializer(serializers.ModelSerializer):
    employee_id = serializers.IntegerField(source="employee.id", read_only=True)
    fullname = serializers.CharField(source="employee.fullname", read_only=True)

    class Meta:
        model = models.Email
        fields = ("id", "employee_id", "fullname", "email", "kind", "notes")


class EmailCreateSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(
        queryset=models.Employee.objects.all(),
    )

    class Meta:
        model = models.Email
        fields = ("email", "employee", "kind", "notes")
