from rest_framework import serializers

from apps.units.myp.models import (
    MypUnitPlanner,
    MypUnitPlannerInterdisciplinary,
    )

# Список планнеров в MYP
class MypUnitPlannerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MypUnitPlanner
        fields = (
            "id",
            "order",
            "title",
            "subject",
            "level",
            "year",
            "hours",
            "global_context"
            )
        
# Список междисциплинарных планеров в MYP
class MypUnitPlannerInterdisciplinaryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MypUnitPlannerInterdisciplinary
        fields = (
            "id",
            "title",
            "year",
            "hours",
            "global_context"
            )