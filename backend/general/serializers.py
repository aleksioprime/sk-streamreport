from rest_framework import serializers
from general.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Кастомный сериализатор для ответа при JWT-авторизации
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Добавление дополнительных данных к токенам
        data['user'] = {
            'email': self.user.email,
            'first_name': self.user.first_name,
            'middle_name': self.user.middle_name,
            'last_name': self.user.last_name,
        }

        return data

# Регистрация пользователя
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "first_name",
            "last_name",
        )

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user