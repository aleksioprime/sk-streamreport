from apps.portfolio.models import (
    EventParticipation,
)

def get_event_participation_queryset():
    return EventParticipation.objects.all().select_related(
        'student', 'group', 'author'
        )