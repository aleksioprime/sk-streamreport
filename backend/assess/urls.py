from django.urls import path
from assess.views import StudyYearViewSet, ClassGroupViewSet, StudyPeriodViewSet, SummativeWorkListViewSet, \
    SummativeWorkItemViewSet, WorkAssessmentViewSet, WorkCriteriaMarkViewSet, StudentViewSet

urlpatterns = [
    path('student', StudentViewSet.as_view({'get': 'list'})),
    path('assessment/year', StudyYearViewSet.as_view({'get': 'list'})),
    path('assessment/group', ClassGroupViewSet.as_view({'get': 'list'})),
    path('assessment/period', StudyPeriodViewSet.as_view({'get': 'list'})),
    path('assessment/sumwork', SummativeWorkListViewSet.as_view({'get': 'list'})),
    path('assessment/sumwork/<int:pk>', SummativeWorkItemViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('assessment/workassess', WorkAssessmentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('assessment/workassess/<int:pk>', WorkAssessmentViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('assessment/workcriteriamark', WorkCriteriaMarkViewSet.as_view({'get': 'list'})),
]