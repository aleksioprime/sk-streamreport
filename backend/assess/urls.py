from django.urls import path
from assess.views import StudyYearViewSet, ClassGroupViewSet, StudyPeriodViewSet, SummativeWorkViewSet, \
    WorkAssessmentViewSet, PeriodAssessmentViewSet, StudentViewSet, WorkGroupDateItemViewSet, \
    StudentWorkViewSet, AssessmentJournalAPIView, ReportPeriodViewSet, StudentReportTeacherViewSet, \
    ReportTeacherViewSet

urlpatterns = [
    path('student', StudentViewSet.as_view({'get': 'list'})),
    path('assessment/year', StudyYearViewSet.as_view({'get': 'list'})),
    path('assessment/group', ClassGroupViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('assessment/group/<int:pk>', ClassGroupViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('assessment/period', StudyPeriodViewSet.as_view({'get': 'list'})),
    path('assessment/report/period', ReportPeriodViewSet.as_view({'get': 'list'})),
    path('assessment/student/report/teacher', StudentReportTeacherViewSet.as_view({'get': 'list'})),
    path('assessment/student', StudentWorkViewSet.as_view({'get': 'list'})),
    path('assessment/sumwork', SummativeWorkViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('assessment/sumwork/<int:pk>', SummativeWorkViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('assessment/workgroup/<int:pk>', WorkGroupDateItemViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('assessment/workassess', WorkAssessmentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('assessment/workassess/<int:pk>', WorkAssessmentViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('assessment/periodassess', PeriodAssessmentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('assessment/periodassess/<int:pk>', PeriodAssessmentViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('assessment/report/teacher', ReportTeacherViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('assessment/report/teacher/<int:pk>', ReportTeacherViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('assessment/journal', AssessmentJournalAPIView.as_view()),
]