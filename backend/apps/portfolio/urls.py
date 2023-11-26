from django.urls import path

from apps.portfolio.views import (
    EventParticipationViewSet
)

urlpatterns = [
    path('portfolio/event/participation', EventParticipationViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('portfolio/event/participation/<int:pk>', EventParticipationViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
]
