from rest_framework import serializers

from apps.units.pyp.models import (
    PypUnitPlanner,
    )

# Список планнеров в PYP
class PypUnitPlannerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PypUnitPlanner
        fields = (
            "id",
            "order",
            "title",
            "teachers",
            "year",
            "hours",
            "transdisciplinary_theme",
            )