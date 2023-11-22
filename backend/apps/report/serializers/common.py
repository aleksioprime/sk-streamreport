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

# Список пользователей для репортов
class UserListReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id", 
            "first_name", 
            "last_name",
            "middle_name",
            )

# Список учебных лет для репортов
class AcademicYearListReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = (
            "id",
            "name",
            "date_start",
            "date_end"
            )

# Список учебных параллелей для репортов
class StudyYearListReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyYear
        fields = (
            "id",
            "number",
            "level",
            )

# Список учебных классов для репортов
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

# Список предметов для репортов
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
        
# Список отчётных периодов для репортов
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

# Просмотр, создание и редактирование уровней достижений по чек-листу
class ReportCriterionLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportCriterionLevel
        fields = '__all__'

# Просмотр чек-листа рефлексии для репортов
class ReportCriterionListSerializer(serializers.ModelSerializer):
    author = UserListReportSerializer()
    subjects = SubjectReportListSerializer(many=True)
    years = StudyYearListReportSerializer(many=True)
    levels = ReportCriterionLevelSerializer(many=True)
    class Meta:
        model = ReportCriterion
        fields = '__all__'

# Создание и редактирование чек-листа рефлексии для репортов
class ReportCriterionUpdateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    class Meta:
        model = ReportCriterion
        fields = '__all__'

# 
class ReportCriterionAchievementListSerializer(serializers.ModelSerializer):
    criterion = ReportCriterionListSerializer()
    achievement = ReportCriterionLevelSerializer()
    class Meta:
        model = ReportCriterionAchievement
        fields = '__all__'

# 
class ReportCriterionAchievementUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportCriterionAchievement
        fields = '__all__'