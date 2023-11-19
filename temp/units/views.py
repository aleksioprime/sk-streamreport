from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated

from apps.units.serializers import (
    PypUnitPlannerListSerializer, 
    MypUnitPlannerListSerializer,
    MypUnitPlannerInterdisciplinaryListSerializer,
    DpUnitPlannerListSerializer,
)

from apps.units.services import (
    get_pyp_unit_planner_queryset,
    get_myp_unit_planner_queryset,
    get_myp_unit_planner_interdisciplinary_queryset,
    get_dp_unit_planner_queryset,
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
    
@extend_schema_view(
    list=extend_schema(summary='Список юнитов в MYP', tags=['Юниты в MYP']),
    )
class MypUnitPlannerViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return MypUnitPlannerListSerializer
    
    def get_queryset(self):
        return get_myp_unit_planner_queryset()
    
@extend_schema_view(
    list=extend_schema(summary='Список междисциплинарных юнитов в MYP', tags=['Юниты в MYP (междисциплинарные)']),
    )
class MypUnitPlannerInterdisciplinaryViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return MypUnitPlannerInterdisciplinaryListSerializer
    
    def get_queryset(self):
        return get_myp_unit_planner_interdisciplinary_queryset()
    
@extend_schema_view(
    list=extend_schema(summary='Список юнитов в DP', tags=['Юниты в DP']),
    )
class DpUnitPlannerViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return DpUnitPlannerListSerializer
    
    def get_queryset(self):
        return get_dp_unit_planner_queryset()