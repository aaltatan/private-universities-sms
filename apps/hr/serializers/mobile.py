from rest_framework import serializers

from .. import models


class MobileSerializer(serializers.ModelSerializer):
    employee_id = serializers.IntegerField(source="employee.id", read_only=True)
    fullname = serializers.SerializerMethodField(
        source="employee.fullname", read_only=True
    )

    class Meta:
        model = models.Mobile
        fields = (
            "id",
            "employee_id",
            "fullname",
            "number",
            "kind",
            "has_whatsapp",
            "notes",
        )


class MobileCreateSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(
        queryset=models.Employee.objects.all(),
    )

    class Meta:
        model = models.Mobile
        fields = ("number", "employee", "kind", "has_whatsapp", "notes")
