from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.ibo.services import (
    get_learner_profile_queryset,
    get_ib_profile_develop_queryset,
    get_unit_reflection_post_queryset
)

from apps.ibo.serializers import (
    LearnerProfileListSerializer,
    IbProfileDevelopUpdateSerializer,
    IbProfileDevelopListSerializer,
    UnitReflectionPostListSerializer,
    UnitReflectionPostUpdateSerializer
)

from apps.ibo.filters import (
    IbProfileDevelopFilter,
    UnitReflectionPostFilter
)

# Качества профиля студента IB: список
@extend_schema_view(
    list=extend_schema(summary='Вывод списка качеств профиля студента IB', tags=['IB: Качества профиля студента']),
    )
class LearnerProfileViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_learner_profile_queryset()
    serializer_class = LearnerProfileListSerializer

# Развитие Ib Learner Profile в юните: список, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка пунктов развития Learner Profile в юните', tags=['IB: Юниты. Развитие Learner Profile']),
    create=extend_schema(summary='Создание пункта развития Learner Profile в юните', tags=['IB: Юниты. Развитие Learner Profile']),
    update=extend_schema(summary='Обновление пункта развития Learner Profile в юните', tags=['IB: Юниты. Развитие Learner Profile']),
    partial_update=extend_schema(summary='Частичное обновление пункта развития Learner Profile в юните', tags=['IB: Юниты. Развитие Learner Profile']),
    destroy=extend_schema(summary='Удаление пункта развития Learner Profile в юните', tags=['IB: Юниты. Развитие Learner Profile']),
    )
class IbProfileDevelopViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_ib_profile_develop_queryset()
    filterset_class = IbProfileDevelopFilter
    
    def get_serializer_class(self):
        if self.action == "list":
            return IbProfileDevelopListSerializer
        return IbProfileDevelopUpdateSerializer
    
    # Переопределение метода partial_update для ответа с другим сериализатором
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        detail_serializer = IbProfileDevelopListSerializer(serializer.instance)
        return Response(detail_serializer.data, status=status.HTTP_200_OK)
    
# Посты рефлексии в юните: список, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка постов рефлексии в юните', tags=['IB: Юниты. Посты рефлексии']),
    create=extend_schema(summary='Создание поста рефлексии в юните', tags=['IB: Юниты. Посты рефлексии']),
    update=extend_schema(summary='Обновление поста рефлексии в юните', tags=['IB: Юниты. Посты рефлексии']),
    partial_update=extend_schema(summary='Частичное обновление поста рефлексии в юните', tags=['IB: Юниты. Посты рефлексии']),
    destroy=extend_schema(summary='Удаление поста рефлексии в юните', tags=['IB: Юниты. Посты рефлексии']),
    )
class UnitReflectionPostViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_unit_reflection_post_queryset()
    filterset_class = UnitReflectionPostFilter
    
    def get_serializer_class(self):
        if self.action == "list":
            return UnitReflectionPostListSerializer
        return UnitReflectionPostUpdateSerializer
    
    # Переопределение метода partial_update для ответа с другим сериализатором
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        detail_serializer = UnitReflectionPostListSerializer(serializer.instance)
        return Response(detail_serializer.data, status=status.HTTP_200_OK)