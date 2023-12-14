from django.urls import path

from apps.ibo.views import (
    LearnerProfileViewSet,
    IbProfileDevelopViewSet,
    UnitReflectionPostViewSet,
    AtlCategoryViewSet
)

urlpatterns = [
    path('ib/profile', LearnerProfileViewSet.as_view({'get': 'list'})),
    path('ib/atl/category', AtlCategoryViewSet.as_view({'get': 'list'})),
    path('ib/unit/profile', IbProfileDevelopViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('ib/unit/profile/<int:pk>', IbProfileDevelopViewSet.as_view({'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('ib/unit/reflection', UnitReflectionPostViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('ib/unit/reflection/<int:pk>', UnitReflectionPostViewSet.as_view({'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
]
