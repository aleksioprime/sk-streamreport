from rest_framework.viewsets import GenericViewSet 
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
import logging

logger = logging.getLogger('main')

from general.serializers import (
    UserRegistrationSerializer, 
    UserListSerializer, 
    UserRetrieveSerializer,
    CustomTokenObtainPairSerializer
)

from general.models import (
    User,
)

@extend_schema_view(post=extend_schema(summary='Получение токена', tags=['Аутентификация']))
class CustomTokenObtainPairView(TokenObtainPairView):
    logger.info("Пользователь вошёл в систему")
    serializer_class = CustomTokenObtainPairSerializer

@extend_schema_view(post=extend_schema(summary='Обновление токена',tags=['Аутентификация']))
class CustomTokenRefreshView(TokenRefreshView):
    pass

class UserViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]

    # переопределение get_queryset с указанием prefetch_related для избежания N + 1
    def get_queryset(self):
        queryset = User.objects.all().prefetch_related(
            "myp_unitplans",
        ).order_by("-id")
        return queryset

    # переопределение сериализатора в зависимости от action
    def get_serializer_class(self):
        if self.action == "create":
            return UserRegistrationSerializer
        if self.action in ["retrieve", "me"]:
            return UserRetrieveSerializer
        return UserListSerializer

    # переопределение значения permission_classes в зависимоси от action
    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny]
        return super().get_permissions()
    
    @extend_schema(summary='Создание нового пользователя', tags=['Пользователи'])
    def create(self, request):
        # your non-standard behaviour
        return super().create(request)
    
    @extend_schema(summary='Вывод списка пользователей', tags=['Пользователи'])
    def list(self, request):
        # your non-standard behaviour
        return super().list(request)
    
    @extend_schema(summary='Вывод информации о конкретном пользователе', tags=['Пользователи'])
    def retrieve(self, request):
        # your non-standard behaviour
        return super().retrieve(request)
    
    @extend_schema(summary='Вывод информации об авторизованном пользователе', tags=['Пользователи'])
    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    # @action(detail=True, methods=["get"])
    # def friends(self, request, pk=None):
    #     user = self.get_object()
    #     queryset = self.filter_queryset(
    #         self.get_queryset().filter(friends=user)
    #     )
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)

    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)