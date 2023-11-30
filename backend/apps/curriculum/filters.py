from admin_auto_filters.filters import AutocompleteFilter
import django_filters

from apps.curriculum.models import (
    Subject,
    Curriculum,
    CurriculumLoad,
    TeachingLoad
)

class SubjectAdminFilter(AutocompleteFilter):
    title = 'Предмет'
    field_name = 'subject'

class SubjectFilter(django_filters.FilterSet):
    curriculum_loads__curriculum = django_filters.AllValuesFilter(field_name='curriculum_loads__curriculum', distinct=True)
    curriculum_loads__years__classes = django_filters.AllValuesFilter(field_name='curriculum_loads__years__classes', distinct=True)
    class Meta:
        model = Subject
        fields = {
            'department',
            'curriculum_loads__curriculum',
            'curriculum_loads__years__classes',
        }

class CurriculumFilter(django_filters.FilterSet):
    class Meta:
        model = Curriculum
        fields = {
            'year',
        }

class CurriculumLoadFilter(django_filters.FilterSet):
    class Meta:
        model = CurriculumLoad
        fields = {
            'curriculum',
            'subject',
            'years'
        }

class TeachingLoadFilter(django_filters.FilterSet):
    class Meta:
        model = TeachingLoad
        fields = {
            'year',
            'teacher',
            'subject',
            'groups'
        }