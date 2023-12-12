from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import Group
from general.models import (
    User,
    Department,
    ClassGroup,
    AcademicYear,
    StudyYear,
    StudyYearIb
    )

# Кастомный сериализатор для ответа при JWT-аутентификации (неактивен)
# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)
#         # Добавление дополнительных данных к токенам
#         data['user'] = {
#             'id': self.user.pk,
#             'email': self.user.email,
#             'first_name': self.user.first_name,
#             'middle_name': self.user.middle_name,
#             'last_name': self.user.last_name,
#         }
#         return data

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
            "middle_name",
            "dnevnik_id",
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
class UserListGeneralSerializer(serializers.ModelSerializer):
    short_name = serializers.CharField(source='get_short_name', read_only=True)
    class Meta:
        model = User
        fields = (
            "id", 
            "first_name", 
            "last_name",
            "middle_name",
            "photo",
            "email",
            "dnevnik_id",
            "position",
            "short_name"
            )

# Список пользователей
class GroupGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            "id", 
            "name",
            )

# Информация о пользователе
class UserRetrieveSerializer(serializers.ModelSerializer):
    groups = GroupGeneralSerializer(many=True)
    departments = DepartmentListSerializer(many=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "full_name",
            "email",
            "gender",
            "position",
            "photo",
            "departments",
            "groups",
            "classes",
            "dnevnik_id",
            "dnevnik_user_id",
        )

# Импорт пользователей
class UserImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "email",
            "gender",
            "password",
            "position",
            "departments",
            "groups",
            "classes",
            "dnevnik_id",
            "dnevnik_user_id",
        )
        extra_kwargs = {
            'departments': {'required': False, 'allow_null': True},
            'classes': {'required': False, 'allow_null': True},
        }

# Учебные года
class AcademicYearListGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = (
            "id",
            "name",
            "date_start",
            "date_end"
            )

# Параллели в IB
class StudyYearIbListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyYearIb
        fields = (
            "id",
            "name",
            "program_ib",
            )
        
# Параллели обучения
class StudyYearListGeneralSerializer(serializers.ModelSerializer):
    ib = StudyYearIbListSerializer()
    level_name = serializers.CharField(source='get_level_display', read_only=True)
    class Meta:
        model = StudyYear
        fields = (
            "id",
            "number",
            "level",
            "ib",
            "level_name",
            "name",
            )
    

# Список групп
class ClassGroupListGeneralSerializer(serializers.ModelSerializer):
    year_academic = AcademicYearListGeneralSerializer()
    year_study = StudyYearListGeneralSerializer()
    mentor = UserListGeneralSerializer()
    class Meta:
        model = ClassGroup
        fields = (
            "id",
            "year_academic",
            "year_study",
            "letter",
            "name",
            "curriculum",
            "mentor",
            )

# Информация о группе
class ClassRetrieveSerializer(serializers.ModelSerializer):
    students = UserListGeneralSerializer(many=True)
    mentor = UserListGeneralSerializer()
    extra = UserListGeneralSerializer(many=True)
    class Meta:
        model = ClassGroup
        fields = (
            "id",
            "year_academic",
            "year_study",
            "year_study_ib",
            "letter",
            "dnevnik_id",
            "students",
            "mentor",
            "extra",
            "curriculum",
        )