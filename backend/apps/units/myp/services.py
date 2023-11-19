from apps.units.myp.models import (
    MypUnitPlanner,
    MypUnitPlannerInterdisciplinary,
    )

def get_myp_unit_planner_queryset():
    return MypUnitPlanner.objects.all().order_by("title")

def get_myp_unit_planner_interdisciplinary_queryset():
    return MypUnitPlannerInterdisciplinary.objects.all().order_by("title")
