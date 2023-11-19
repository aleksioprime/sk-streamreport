from rest_framework.routers import SimpleRouter
from apps.units.views import (
    PypUnitPlannerViewSet,
    MypUnitPlannerViewSet,
    MypUnitPlannerInterdisciplinaryViewSet,
    DpUnitPlannerViewSet,
    )

router = SimpleRouter()
router.register(r'units/pyp', PypUnitPlannerViewSet, basename="pyp_unit_planner")
router.register(r'units/myp', MypUnitPlannerViewSet, basename="myp_unit_planner")
router.register(r'units/myp/idu', MypUnitPlannerInterdisciplinaryViewSet, basename="myp_unit_planner_id")
router.register(r'units/dp', DpUnitPlannerViewSet, basename="dp_unit_planner")

urlpatterns = router.urls