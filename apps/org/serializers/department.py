from rest_framework import serializers

from .. import models


class DepartmentSerializer(serializers.ModelSerializer):
    class CostCenterSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.Department
            fields = ("id", "name", "description")

    cost_center = CostCenterSerializer(read_only=True)

    class Meta:
        model = models.Department
        fields = ("id", "name", "description", "cost_center")


class DepartmentActivitySerializer(serializers.ModelSerializer):
    cost_center = serializers.CharField(source="cost_center.name")
    parent = serializers.CharField(source="parent.name")

    class Meta:
        model = models.Department
        fields = ("name", "cost_center", "parent", "description")


class CreateUpdateDepartmentSerializer(serializers.ModelSerializer):
    cost_center = serializers.PrimaryKeyRelatedField(
        queryset=models.CostCenter.objects.all(),
    )
    parent = serializers.PrimaryKeyRelatedField(
        queryset=models.Department.objects.all(),
    )

    class Meta:
        model = models.Department
        fields = ("name", "cost_center", "parent", "description")
