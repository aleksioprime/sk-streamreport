from django.urls import path

from apps.curriculum.views import (
    SubjectViewSet,
    CurriculumViewSet,
    CurriculumLoadViewSet,
    TeachingLoadViewSet
    )

urlpatterns = [
    path('subject', SubjectViewSet.as_view({'get': 'list'})),
    path('curriculum', CurriculumViewSet.as_view({'get': 'list'})),
    path('curriculum/<int:pk>', CurriculumViewSet.as_view({'get': 'retrieve'})),
    path('curriculum/load', CurriculumLoadViewSet.as_view({'get': 'list'})),
    path('curriculum/teaching', TeachingLoadViewSet.as_view({'get': 'list'})),
]