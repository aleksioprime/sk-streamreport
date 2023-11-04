from rest_framework.viewsets import GenericViewSet 
from rest_framework.mixins import CreateModelMixin
from general.serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = UserRegistrationSerializer
    @extend_schema(
            summary='Создает нового пользователя', 
            description='Создание пользователя'
            )
    def create(self, request):
        # your non-standard behaviour
        return super().create(request)