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
class UserListReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id", 
            "first_name", 
            "last_name",
            "middle_name",
            )

# Список учебных лет
class AcademicYearListReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = (
            "id",
            "name",
            "date_start",
            "date_end"
            )

# Список учебных параллелей
class StudyYearListReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyYear
        fields = (
            "id",
            "number",
            "level",
            )

# Список учебных классов
class ClassGroupListReportSerializer(serializers.ModelSerializer):
    year_academic = AcademicYearListReportSerializer()
    year_study = StudyYearListReportSerializer()
    class Meta:
        model = ClassGroup
        fields = (
            "id",
            "year_academic",
            "year_study",
            "letter",
            )

# Список предметов
class SubjectReportListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = (
            "id", 
            "name", 
            "name_eng",
            "level",
            "need_report"
            )
        
# Вывод списка отчётных периодов для репортов
class ReportPeriodListSerializer(serializers.ModelSerializer):
    year = AcademicYearListReportSerializer()
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
    author = UserListReportSerializer()
    subjects = SubjectReportListSerializer(many=True)
    years = StudyYearListReportSerializer(many=True)
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