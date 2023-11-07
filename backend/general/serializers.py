from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from general.models import (
    User,
    Department,
    )

# Кастомный сериализатор для ответа при JWT-аутентификации
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Добавление дополнительных данных к токенам
        data['user'] = {
            'id': self.user.pk,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'middle_name': self.user.middle_name,
            'last_name': self.user.last_name,
        }
        return data

# Подразделения
class DepartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ("id", "name", "logo")

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

# Список пользователей
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name")

# Информация о конкретном пользователей
class UserRetrieveSerializer(serializers.ModelSerializer):
    myp_unitplans_count = serializers.SerializerMethodField()
    departments = DepartmentListSerializer(many=True)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "myp_unitplans_count",
            "departments"
        )
        
    def get_myp_unitplans_count(self, obj) -> int:
        return obj.myp_unitplans.count()