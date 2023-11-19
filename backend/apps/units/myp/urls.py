from rest_framework.routers import SimpleRouter

from apps.units.myp.views import (
    MypUnitPlannerViewSet,
    MypUnitPlannerInterdisciplinaryViewSet,
    )

router = SimpleRouter()
router.register(r'units/myp', MypUnitPlannerViewSet, basename="myp_unit_planner")
router.register(r'units/myp/idu', MypUnitPlannerInterdisciplinaryViewSet, basename="myp_unit_planner_id")

urlpatterns = router.urls