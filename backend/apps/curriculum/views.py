from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status

from apps.curriculum.serializers import (
    SubjectListSerializer, 
    CurriculumListSerializer,
    CurriculumRetrieveSerializer,
    CurriculumLoadListSerializer,
    TeachingLoadListSerializer,
    TeachingLoadUpdateSerializer,
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
    retrieve=extend_schema(summary='Просмотр учебного плана', tags=['Учебные планы']),
    )
class CurriculumViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    filterset_class = CurriculumFilter
    pagination_class = None

    def get_queryset(self):
        return get_curriculum_queryset()
    
    def get_serializer_class(self):
        if self.action == "retrieve":
            return CurriculumRetrieveSerializer
        return CurriculumListSerializer

@extend_schema_view(
    list=extend_schema(summary='Список предметов', tags=['Учебные планы: Предметы']),
    )
class SubjectViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    filterset_class = SubjectFilter
    pagination_class = None
    
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
class TeachingLoadViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    filterset_class = TeachingLoadFilter

    def get_queryset(self):
        return get_teaching_load_queryset()

    def get_serializer_class(self):
        if self.action == "list":
            return TeachingLoadListSerializer
        return TeachingLoadUpdateSerializer
    
    # Переопределение метода create для массового создания объектов
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        if isinstance(serializer.instance, list):
            data = [TeachingLoadListSerializer(instance).data for instance in serializer.instance]
        else:
            data = TeachingLoadListSerializer(serializer.instance).data
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
    
    # Переопределение метода partial_update для ответа с другим сериализатором
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        detail_serializer = TeachingLoadListSerializer(serializer.instance)
        return Response(detail_serializer.data, status=status.HTTP_200_OK)
    
    
