import django_filters

from general.models import (
    ClassGroup,
    User
)

class ClassGroupFilter(django_filters.FilterSet):
    year_study__curriculum_loads__curriculum = django_filters.AllValuesFilter(field_name='year_study__curriculum_loads__curriculum', distinct=True)
    class Meta:
        model = ClassGroup
        fields = {
            'year_academic',
            'year_study',
            'year_study__curriculum_loads__curriculum'
        }

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = {
            'groups',
            'classes'
        }