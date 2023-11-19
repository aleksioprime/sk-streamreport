from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from general.models import (
    User,
    Department,
    ClassGroup,
    AcademicYear,
    StudyYear,
    StudyYearIb
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
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id", 
            "first_name", 
            "last_name",
            "middle_name",
            "email",
            "dnevnik_id",
            )

# Информация о пользователе
class UserRetrieveSerializer(serializers.ModelSerializer):
    myp_unitplans_count = serializers.SerializerMethodField()
    departments = DepartmentListSerializer(many=True)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "email",
            "gender",
            "position",
            "departments",
            "groups",
            "classes",
            "dnevnik_id",
            "dnevnik_user_id",
            "myp_unitplans_count"
        )
        
    def get_myp_unitplans_count(self, obj) -> int:
        return obj.myp_unitplans.count()

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
class AcademicYearListSerializer(serializers.ModelSerializer):
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
class StudyYearListSerializer(serializers.ModelSerializer):
    ib = StudyYearIbListSerializer()
    class Meta:
        model = StudyYear
        fields = (
            "id",
            "number",
            "level",
            "ib",
            )

# Список групп
class ClassGroupListSerializer(serializers.ModelSerializer):
    year_academic = AcademicYearListSerializer()
    year_study = StudyYearListSerializer()
    class Meta:
        model = ClassGroup
        fields = (
            "id",
            "year_academic",
            "year_study",
            "letter",
            )

# Информация о группе
class ClassCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassGroup
        fields = (
            "id",
            "year_academic",
            "year_study",
            "year_study_ib",
            "letter",
            "dnevnik_id",
            "mentor",
            "extra",
        )

# Информация о группе со студентами
class ClassRetrieveSerializer(serializers.ModelSerializer):
    students = UserListSerializer(many=True)
    mentor = UserListSerializer()
    extra = UserListSerializer(many=True)
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
        )