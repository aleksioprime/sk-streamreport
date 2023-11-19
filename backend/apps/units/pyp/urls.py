from rest_framework.routers import SimpleRouter

from apps.units.pyp.views import (
    PypUnitPlannerViewSet,
    )

router = SimpleRouter()
router.register(r'units/pyp', PypUnitPlannerViewSet, basename="pyp_unit_planner")

urlpatterns = router.urls