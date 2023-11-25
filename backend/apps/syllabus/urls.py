from django.urls import path

from apps.syllabus.views import (
    CourseTopicViewSet,
    SyllabusViewSet
)

urlpatterns = [
    path('syllabus', SyllabusViewSet.as_view({'get': 'list'})),
    path('syllabus/<int:pk>', SyllabusViewSet.as_view({'get': 'retrieve'})),
    path('syllabus/course/topic', CourseTopicViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('syllabus/course/topic/<int:pk>', CourseTopicViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
]
