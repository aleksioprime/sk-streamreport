from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from apps.curriculum.serializers import (
    SubjectListSerializer, 
    CurriculumLoadListSerializer,
    TeachingLoadListSerializer,
)

from apps.curriculum.services import (
    get_subject_queryset,
    get_curriculum_load_queryset,
    get_teaching_load_queryset
)

from apps.curriculum.filters import (
    SubjectViewFilter
)

@extend_schema_view(
    list=extend_schema(summary='Список предметов', tags=['Предметы']),
    )
class SubjectViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    filterset_class = SubjectViewFilter

    def get_serializer_class(self):
        return SubjectListSerializer
    
    def get_queryset(self):
        return get_subject_queryset()
    
@extend_schema_view(
    list=extend_schema(summary='Список нагрузки учебных планов', tags=['Нагрузка учебных планов']),
    )
class CurriculumLoadViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return CurriculumLoadListSerializer
    
    def get_queryset(self):
        return get_curriculum_load_queryset()
    
@extend_schema_view(
    list=extend_schema(summary='Список нагрузки учителей', tags=['Нагрузка учителей']),
    )
class TeachingLoadViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return TeachingLoadListSerializer
    
    def get_queryset(self):
        return get_teaching_load_queryset()
