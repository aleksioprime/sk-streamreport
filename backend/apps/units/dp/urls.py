from django.urls import path

from apps.units.dp.views import (
    DpUnitPlannerViewSet,
    DpAimViewSet,
    DpObjectiveViewSet,
    CourseContentViewSet,
    CriterionViewSet,
    DpAtlSkillViewSet,
    DpInquiryQuestionViewSet,
    DpAtlDevelopViewSet,
    )

urlpatterns = [
    path('dp/aim', DpAimViewSet.as_view({'get': 'list'})),
    path('dp/objective', DpObjectiveViewSet.as_view({'get': 'list'})),
    path('dp/content', CourseContentViewSet.as_view({'get': 'list'})),
    path('dp/criterion', CriterionViewSet.as_view({'get': 'list'})),
    path('dp/atl', DpAtlSkillViewSet.as_view({'get': 'list'})),
    path('dp/unit', DpUnitPlannerViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('dp/unit/<int:pk>', DpUnitPlannerViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('dp/unit/inquiry', DpInquiryQuestionViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('dp/unit/inquiry/<int:pk>', DpInquiryQuestionViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('dp/unit/atl', DpAtlDevelopViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('dp/unit/atl/<int:pk>', DpAtlDevelopViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
]