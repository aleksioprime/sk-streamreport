from django.urls import path

from apps.ibo.views import (
    LearnerProfileViewSet,
)

urlpatterns = [
    path('ib/profile', LearnerProfileViewSet.as_view({'get': 'list'})),
]
