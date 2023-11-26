from rest_framework import serializers

from apps.portfolio.models import (
    EventParticipation,
)

from general.models import (
    User,
    AcademicYear,
    ClassGroup,
    StudyYear,
    )

# Список пользователей
class UserPortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id", 
            "first_name", 
            "last_name",
            "middle_name",
            )

# Список учебных лет
class AcademicYearPortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = (
            "id",
            "name",
            "date_start",
            "date_end"
            )

# Список учебных параллелей
class StudyYearPortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyYear
        fields = (
            "id",
            "number",
            "level",
            )

# Список учебных классов
class ClassGroupPortfolioSerializer(serializers.ModelSerializer):
    year_academic = AcademicYearPortfolioSerializer()
    year_study = StudyYearPortfolioSerializer()
    class Meta:
        model = ClassGroup
        fields = (
            "id",
            "year_academic",
            "year_study",
            "letter",
            )     

# Вывод списка участий студентов в мероприятиях
class EventParticipationListSerializer(serializers.ModelSerializer):
    student = UserPortfolioSerializer()
    author = UserPortfolioSerializer()
    group = ClassGroupPortfolioSerializer()
    class Meta:
        model = EventParticipation
        fields = (
            "id", 
            "student",
            "group",
            "author",
            "title",
            "result",
            "created_at",
            "updated_at",
            )

# Создание и редактирование участия студента в мероприятии
class EventParticipationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventParticipation
        fields = '__all__'