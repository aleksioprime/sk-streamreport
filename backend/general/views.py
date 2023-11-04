from rest_framework.viewsets import GenericViewSet 
from rest_framework.mixins import CreateModelMixin
from general.serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample, OpenApiResponse
from rest_framework_simplejwt.views import TokenObtainPairView

@extend_schema_view(
    post=extend_schema(
        tags=['Аутентификация'],
    )
)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@extend_schema_view(
    create=extend_schema(
        responses={
            200: UserRegistrationSerializer,
        }
    )
)
class UserViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = UserRegistrationSerializer
    @extend_schema(
            summary='Создает нового пользователя', 
            description='Описание функции создания пользователя',
            tags=['Пользователи']
            )
    def create(self, request):
        # your non-standard behaviour
        return super().create(request)