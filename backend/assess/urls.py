from django.urls import path
from assess.views import StudyYearViewSet, ClassGroupViewSet, StudyPeriodViewSet, SummativeWorkViewSet, \
    WorkAssessmentViewSet, WorkCriteriaMarkViewSet

urlpatterns = [
    path('assessment/year', StudyYearViewSet.as_view({'get': 'list'})),
    path('assessment/group', ClassGroupViewSet.as_view({'get': 'list'})),
    path('assessment/period', StudyPeriodViewSet.as_view({'get': 'list'})),
    path('assessment/sumwork', SummativeWorkViewSet.as_view({'get': 'list'})),
    path('assessment/workassess', WorkAssessmentViewSet.as_view({'get': 'list'})),
    path('assessment/workcriteriamark', WorkCriteriaMarkViewSet.as_view({'get': 'list'})),
]