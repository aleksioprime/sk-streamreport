import django_filters

from apps.portfolio.models import (
    EventParticipation,
)

class EventParticipationFilter(django_filters.FilterSet):
    class Meta:
        model = EventParticipation
        fields = {'student', 'group'}