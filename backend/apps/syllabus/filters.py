import django_filters

from apps.syllabus.models import (
    Syllabus,
    CourseTopic
)

class SyllabusFilter(django_filters.FilterSet):
    class Meta:
        model = Syllabus
        fields = {'subject', 'years'}

class CourseTopicFilter(django_filters.FilterSet):
    class Meta:
        model = CourseTopic
        fields = {'chapter'}