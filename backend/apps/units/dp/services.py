from apps.units.dp.models import (
    DpUnitPlanner,
    )

def get_dp_unit_planner_queryset():
    return DpUnitPlanner.objects.all().order_by("title")