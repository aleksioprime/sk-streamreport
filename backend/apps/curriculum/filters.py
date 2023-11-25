from admin_auto_filters.filters import AutocompleteFilter
import django_filters

from apps.curriculum.models import (
    Subject
)

class SubjectFilter(AutocompleteFilter):
    title = 'Предмет'
    field_name = 'subject'

class SubjectViewFilter(django_filters.FilterSet):
    class Meta:
        model = Subject
        fields = {
            'department',
        }