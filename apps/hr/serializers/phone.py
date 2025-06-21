from rest_framework import serializers

from .. import models


class PhoneSerializer(serializers.ModelSerializer):
    employee_id = serializers.IntegerField(source="employee.id", read_only=True)
    fullname = serializers.CharField(source="employee.fullname", read_only=True)

    class Meta:
        model = models.Phone
        fields = ("id", "employee_id", "fullname", "number", "kind", "notes")


class PhoneCreateSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(
        queryset=models.Employee.objects.all(),
    )

    class Meta:
        model = models.Phone
        fields = ("number", "employee", "kind", "notes")
