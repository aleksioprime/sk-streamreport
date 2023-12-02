from rest_framework import serializers

from apps.report.models import (
    ReportPeriod,
    ReportCriterion,
    ReportCriterionLevel,
    ReportCriterionAchievement
    )

from general.models import (
    User,
    AcademicYear,
    ClassGroup,
    StudyYear,
    )

from apps.curriculum.models import (
    Subject
    )

# Список пользователей
class UserReportSerializer(serializers.ModelSerializer):
    short_name = serializers.CharField(source='get_short_name', read_only=True)
    class Meta:
        model = User
        fields = (
            "id", 
            "first_name", 
            "last_name",
            "middle_name",
            "short_name",
            )

# Список учебных лет
class AcademicYearReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = (
            "id",
            "name",
            "date_start",
            "date_end"
            )

# Список учебных параллелей
class StudyYearReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyYear
        fields = (
            "id",
            "number",
            "level",
            )

# Список учебных классов
class ClassGroupReportSerializer(serializers.ModelSerializer):
    year_academic = AcademicYearReportSerializer()
    year_study = StudyYearReportSerializer()
    class Meta:
        model = ClassGroup
        fields = (
            "id",
            "year_academic",
            "year_study",
            "letter",
            )

# Список предметов
class SubjectReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = (
            "id", 
            "name", 
            "name_eng",
            "level",
            "need_report",
            "group_ib",
            "discipline_ib"
            )
        
# Вывод списка отчётных периодов для репортов
class ReportPeriodListSerializer(serializers.ModelSerializer):
    year = AcademicYearReportSerializer()
    class Meta:
        model = ReportPeriod
        fields = (
            "id",
            "order",
            "name",
            "year",
            "date_start",
            "date_end",
            )
        
# Создание и редактирование отчётных периодов для репортов
class ReportPeriodUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportPeriod
        fields = '__all__'

# Вывод списка, создание и редактирование уровней достижений по критерию
class ReportCriterionLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportCriterionLevel
        fields = '__all__'

# Вывод списка критериев для репортов
class ReportCriterionListSerializer(serializers.ModelSerializer):
    author = UserReportSerializer()
    subjects = SubjectReportSerializer(many=True)
    years = StudyYearReportSerializer(many=True)
    levels = ReportCriterionLevelSerializer(many=True)
    class Meta:
        model = ReportCriterion
        fields = '__all__'

# Создание и редактирование критериев для репортов
class ReportCriterionUpdateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    class Meta:
        model = ReportCriterion
        fields = '__all__'

# Вывод списка достижений по критериям для репортов учителя
class ReportCriterionAchievementListSerializer(serializers.ModelSerializer):
    criterion = ReportCriterionListSerializer()
    achievement = ReportCriterionLevelSerializer()
    class Meta:
        model = ReportCriterionAchievement
        fields = '__all__'

# Создание и редактирование достижения по критериям для репортов учителя
class ReportCriterionAchievementUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportCriterionAchievement
        fields = '__all__'
    
    # Переопределение метода для создания нескольких объектов
    def create(self, validated_data):
        # Проверка, является ли validated_data списком
        if isinstance(validated_data, list):
            objects_to_create = [ReportCriterionAchievement(**item) for item in validated_data]
            return ReportCriterionAchievement.objects.bulk_create(objects_to_create)
        return ReportCriterionAchievement.objects.create(**validated_data)