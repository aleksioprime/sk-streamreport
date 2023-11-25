from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated

from apps.ibo.services import (
    get_learner_profile_queryset
)

from apps.ibo.serializers import (
    LearnerProfileListSerializer
)

# Качества профиля студента IB: список
@extend_schema_view(
    list=extend_schema(summary='Вывод списка качеств профиля студента IB', tags=['IB: Качества профиля студента']),
    )
class LearnerProfileViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_learner_profile_queryset()
    serializer_class = LearnerProfileListSerializer
