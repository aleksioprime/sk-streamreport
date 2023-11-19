from rest_framework.routers import SimpleRouter
from apps.curriculum.views import (
    SubjectViewSet,
    CurriculumLoadViewSet,
    TeachingLoadViewSet
    )

router = SimpleRouter()
router.register(r'subjects', SubjectViewSet, basename="subjects")
router.register(r'curriculum/loads', CurriculumLoadViewSet, basename="curriculum_load")
router.register(r'teaching/loads', TeachingLoadViewSet, basename="teaching_load")

urlpatterns = router.urls