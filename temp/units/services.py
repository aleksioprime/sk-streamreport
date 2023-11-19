from apps.units.models import (
    PypUnitPlanner,
    MypUnitPlanner,
    MypUnitPlannerInterdisciplinary,
    DpUnitPlanner,
    )

def get_pyp_unit_planner_queryset():
    return PypUnitPlanner.objects.all().order_by("title")

def get_myp_unit_planner_queryset():
    return MypUnitPlanner.objects.all().order_by("title")

def get_myp_unit_planner_interdisciplinary_queryset():
    return MypUnitPlannerInterdisciplinary.objects.all().order_by("title")

def get_dp_unit_planner_queryset():
    return DpUnitPlanner.objects.all().order_by("title")