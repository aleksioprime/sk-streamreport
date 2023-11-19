from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated

from apps.units.pyp.serializers import (
    PypUnitPlannerListSerializer, 
)

from apps.units.pyp.services import (
    get_pyp_unit_planner_queryset,
)

@extend_schema_view(
    list=extend_schema(summary='Список юнитов в PYP', tags=['Юниты в PYP']),
    )
class PypUnitPlannerViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return PypUnitPlannerListSerializer
    
    def get_queryset(self):
        return get_pyp_unit_planner_queryset()
