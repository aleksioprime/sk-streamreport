from admin_auto_filters.filters import AutocompleteFilter
import django_filters

from apps.syllabus.models import (
    Syllabus,
    Course,
    CourseChapter,
    CourseTopic
)

class SubjectAdminFilter(AutocompleteFilter):
    title = 'Предмет'
    field_name = 'subject'

class SyllabusFilter(django_filters.FilterSet):
    class Meta:
        model = Syllabus
        fields = {'subject', 'years'}

class CourseFilter(django_filters.FilterSet):
    class Meta:
        model = Course
        fields = {'year', 'syllabus__subject'}

class CourseTopicFilter(django_filters.FilterSet):
    class Meta:
        model = CourseTopic
        fields = {'chapter'}

class CourseChapterFilter(django_filters.FilterSet):
    class Meta:
        model = CourseChapter
        fields = {'course', 'unit'}

