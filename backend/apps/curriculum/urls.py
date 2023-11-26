from django.urls import path

from apps.curriculum.views import (
    SubjectViewSet,
    CurriculumViewSet,
    CurriculumLoadViewSet,
    TeachingLoadViewSet
    )

urlpatterns = [
    path('curriculum', CurriculumViewSet.as_view({'get': 'list'})),
    path('curriculum/subject', SubjectViewSet.as_view({'get': 'list'})),
    path('curriculum/load', CurriculumLoadViewSet.as_view({'get': 'list'})),
    path('curriculum/teaching', TeachingLoadViewSet.as_view({'get': 'list'})),
]