from rest_framework.routers import SimpleRouter

from apps.report.views import (
    ReportTeacherPrimaryViewSet
    )

router = SimpleRouter()
router.register(r'reports/teacher/primary', ReportTeacherPrimaryViewSet, basename="reports")

urlpatterns = router.urls