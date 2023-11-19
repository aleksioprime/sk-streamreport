from apps.units.pyp.models import (
    PypUnitPlanner,
    )

def get_pyp_unit_planner_queryset():
    return PypUnitPlanner.objects.all().order_by("title")