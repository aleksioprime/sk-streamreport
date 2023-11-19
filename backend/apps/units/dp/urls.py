from rest_framework.routers import SimpleRouter

from apps.units.dp.views import (
    DpUnitPlannerViewSet,
    )

router = SimpleRouter()
router.register(r'units/dp', DpUnitPlannerViewSet, basename="dp_unit_planner")

urlpatterns = router.urls