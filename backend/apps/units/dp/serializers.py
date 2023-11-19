from rest_framework import serializers

from apps.units.dp.models import (
    DpUnitPlanner,
    )

# Список планеров в DP
class DpUnitPlannerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DpUnitPlanner
        fields = (
            "id",
            "order",
            "title",
            "year",
            "authors",
            "teachers",
            "hours",
            "levels",
            )