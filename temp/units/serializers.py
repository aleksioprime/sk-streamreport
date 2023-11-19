from rest_framework import serializers

from apps.units.models import (
    PypUnitPlanner,
    MypUnitPlanner,
    MypUnitPlannerInterdisciplinary,
    DpUnitPlanner,
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