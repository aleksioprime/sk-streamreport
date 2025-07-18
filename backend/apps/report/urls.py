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
    ReportIbProfileViewSet,
    ReportMentorViewSet,
    ReportPrimaryUnitViewSet,
    ReportMentorPrimaryViewSet,
    ReportExtraViewSet,
    UserReportExtraViewSet,
    UserReportMentorPrimaryViewSet,
    UserReportMentorViewSet
    )

urlpatterns = [
    path('report/period', ReportPeriodViewSet.as_view({'get': 'list'})),
    path('report/criterion', ReportCriterionViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('report/criterion/<int:pk>', ReportCriterionViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('report/criterion/level', ReportCriterionLevelViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('report/criterion/levels/<int:pk>', ReportCriterionLevelViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('report/teacher/achievement', ReportCriterionAchievementViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('report/teacher/achievement/<int:pk>', ReportCriterionAchievementViewSet.as_view({'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('report/teacher/primary', ReportTeacherPrimaryViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('report/teacher/primary/<int:pk>', ReportTeacherPrimaryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('report/teacher/primary/topic', ReportPrimaryTopicViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('report/teacher/primary/topic/<int:pk>', ReportPrimaryTopicViewSet.as_view({'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('report/teacher/secondary', ReportTeacherSecondaryViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('report/teacher/secondary/<int:pk>', ReportTeacherSecondaryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('report/teacher/secondary/criterion', ReportSecondaryCriterionViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('report/teacher/secondary/criterion/<int:pk>', ReportSecondaryCriterionViewSet.as_view({'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('report/teacher/secondary/level', ReportSecondaryLevelViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('report/teacher/secondary/level/<int:pk>', ReportSecondaryLevelViewSet.as_view({'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('report/teacher/high', ReportTeacherHighViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('report/teacher/high/<int:pk>', ReportTeacherHighViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('report/mentor', ReportMentorViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('report/mentor/<int:pk>', ReportMentorViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('report/mentor/<int:pk>/export', ReportMentorViewSet.as_view({'get': 'report_export_word'})),
    path('report/mentor/ibprofile', ReportIbProfileViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('report/mentor/ibprofile/<int:pk>', ReportIbProfileViewSet.as_view({'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('report/mentor/primary', ReportMentorPrimaryViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('report/mentor/primary/<int:pk>', ReportMentorPrimaryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('report/mentor/primary/<int:pk>/export', ReportMentorPrimaryViewSet.as_view({'get': 'report_export_word'})),
    path('report/mentor/primary/unit', ReportPrimaryUnitViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('report/mentor/primary/unit/<int:pk>', ReportPrimaryUnitViewSet.as_view({'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('report/extra', ReportExtraViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('report/extra/<int:pk>', ReportExtraViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('report/extra/student', UserReportExtraViewSet.as_view({'get': 'list'})),
    path('report/mentor/student', UserReportMentorViewSet.as_view({'get': 'list'})),
    path('report/mentor/student/<int:pk>/export', UserReportMentorViewSet.as_view({'get': 'report_export_word'})),
    path('report/mentor/primary/student', UserReportMentorPrimaryViewSet.as_view({'get': 'list'})),
]