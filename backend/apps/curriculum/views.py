from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from apps.curriculum.serializers import (
    SubjectListSerializer, 
    CurriculumListSerializer,
    CurriculumLoadListSerializer,
    TeachingLoadListSerializer,
)

from apps.curriculum.services import (
    get_subject_queryset,
    get_curriculum_load_queryset,
    get_teaching_load_queryset,
    get_curriculum_queryset
)

from apps.curriculum.filters import (
    SubjectFilter,
    CurriculumFilter,
    CurriculumLoadFilter,
    TeachingLoadFilter,

)

@extend_schema_view(
    list=extend_schema(summary='Список учебных планов', tags=['Учебные планы']),
    )
class CurriculumViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    filterset_class = CurriculumFilter

    def get_queryset(self):
        return get_curriculum_queryset()
    
    def get_serializer_class(self):
        return CurriculumListSerializer

@extend_schema_view(
    list=extend_schema(summary='Список предметов', tags=['Учебные планы: Предметы']),
    )
class SubjectViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    filterset_class = SubjectFilter
    
    def get_queryset(self):
        return get_subject_queryset()

    def get_serializer_class(self):
        return SubjectListSerializer
    
@extend_schema_view(
    list=extend_schema(summary='Список нагрузки учебных планов', tags=['Учебные планы: Нагрузка предметов']),
    )
class CurriculumLoadViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    filterset_class = CurriculumLoadFilter

    def get_queryset(self):
        return get_curriculum_load_queryset()
    
    def get_serializer_class(self):
        return CurriculumLoadListSerializer
    
    
@extend_schema_view(
    list=extend_schema(summary='Список нагрузки учителей', tags=['Ученые планы: Нагрузка учителей']),
    )
class TeachingLoadViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    filterset_class = TeachingLoadFilter

    def get_queryset(self):
        return get_teaching_load_queryset()

    def get_serializer_class(self):
        return TeachingLoadListSerializer
    
    
