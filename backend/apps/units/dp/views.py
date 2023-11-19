from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated

from apps.units.dp.serializers import (
    DpUnitPlannerListSerializer,
)

from apps.units.dp.services import (
    get_dp_unit_planner_queryset,
)

@extend_schema_view(
    list=extend_schema(summary='Список юнитов в DP', tags=['Юниты в DP']),
    )
class DpUnitPlannerViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return DpUnitPlannerListSerializer
    
    def get_queryset(self):
        return get_dp_unit_planner_queryset()
