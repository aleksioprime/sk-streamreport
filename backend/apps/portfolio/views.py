from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated

from apps.portfolio.services import (
    get_event_participation_queryset,
)

from apps.portfolio.serializers import (
    EventParticipationListSerializer,
    EventParticipationUpdateSerializer

)

from apps.portfolio.filters import (
    EventParticipationFilter,
)

# Участия студентов в мероприятиях: список, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка участий студентов в мероприятиях', tags=['Портфолио: Участие в мероприятиях']),
    create=extend_schema(summary='Создание участия студента в мероприятии', tags=['Портфолио: Участие в мероприятиях']),
    update=extend_schema(summary='Обновление участия студента в мероприятии', tags=['Портфолио: Участие в мероприятиях']),
    destroy=extend_schema(summary='Удаление участия студента в мероприятии', tags=['Портфолио: Участие в мероприятиях']),
    )
class EventParticipationViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_event_participation_queryset()
    filterset_class = EventParticipationFilter
    
    def get_serializer_class(self):
        if self.action == "list":
            return EventParticipationListSerializer
        return EventParticipationUpdateSerializer