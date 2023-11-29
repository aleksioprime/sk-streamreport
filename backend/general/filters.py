import django_filters

from general.models import (
    ClassGroup
)

class ClassGroupFilter(django_filters.FilterSet):
    class Meta:
        model = ClassGroup
        fields = {
            'year_academic',
            'year_study'
        }