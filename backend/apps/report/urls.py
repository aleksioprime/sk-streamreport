from django.urls import path

from apps.report.views import (
    ReportPeriodViewSet,
    ReportCriterionViewSet,
    ReportCriterionLevelViewSet,
    ReportCriterionAchievementViewSet,
    ReportTeacherPrimaryViewSet,
    ReportPrimaryTopicViewSet,
    ReportTeacherSecondaryViewSet,
    ReportSecondaryCriterionViewSet,
    ReportSecondaryLevelViewSet,
    ReportTeacherHighViewSet,
    )

urlpatterns = [
    path('reports/period', ReportPeriodViewSet.as_view({'get': 'list'})),
    path('reports/criterion', ReportCriterionViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('reports/criterion/<int:pk>', ReportCriterionViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('reports/criterion/level', ReportCriterionLevelViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('reports/criterion/levels/<int:pk>', ReportCriterionLevelViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('reports/teacher/achievement', ReportCriterionAchievementViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('reports/teacher/achievement/<int:pk>', ReportCriterionAchievementViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('reports/teacher/primary', ReportTeacherPrimaryViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('reports/teacher/primary/<int:pk>', ReportTeacherPrimaryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('reports/teacher/primary/topic', ReportPrimaryTopicViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('reports/teacher/primary/topic/<int:pk>', ReportPrimaryTopicViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('reports/teacher/secondary', ReportTeacherSecondaryViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('reports/teacher/secondary/<int:pk>', ReportTeacherSecondaryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('reports/teacher/secondary/criterion', ReportSecondaryCriterionViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('reports/teacher/secondary/criterion/<int:pk>', ReportSecondaryCriterionViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('reports/teacher/secondary/level', ReportSecondaryLevelViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('reports/teacher/secondary/level/<int:pk>', ReportSecondaryLevelViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('reports/teacher/high', ReportTeacherHighViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('reports/teacher/high/<int:pk>', ReportTeacherHighViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
]