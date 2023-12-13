from rest_framework import serializers

from apps.report.models import (
    ReportExtra
    )

from .common import (
    UserReportSerializer,
    ClassGroupReportSerializer,
    ReportPeriodListSerializer,
    StudentReportSerializer,
    EventParticipationReportSerializer,
    ReportCriterionAchievementListSerializer,
)

from general.models import (
    User
)

# Вывод списка репортов дополнительных сотрудников класса
class ReportExtraListSerializer(serializers.ModelSerializer):
    student = StudentReportSerializer()
    author = UserReportSerializer()
    group = ClassGroupReportSerializer()
    period = ReportPeriodListSerializer()
    criterion_achievements = ReportCriterionAchievementListSerializer(many=True)
    class Meta:
        model = ReportExtra
        fields = (
            "id",
            "student",
            "author",
            "period",
            "group",
            "comment",
            "created_at",
            "updated_at",
            "criterion_achievements",
            "role",
            )

# Подробный просмотр репорта дополнительных сотрудников класса
class ReportExtraRetrieveSerializer(serializers.ModelSerializer):
    student = StudentReportSerializer()
    author = UserReportSerializer()
    group = ClassGroupReportSerializer()
    period = ReportPeriodListSerializer()
    class Meta:
        model = ReportExtra
        fields = (
            "id",
            "student",
            "author",
            "period",
            "group",
            "comment",
            "created_at",
            "updated_at",
            "role",
            )
        
# Создание и редактирование репорта дополнительных сотрудников класса
class ReportExtraUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportExtra
        fields = '__all__'


class ReportExtraSerializer(serializers.ModelSerializer):
    author = UserReportSerializer()
    student = StudentReportSerializer()
    group = ClassGroupReportSerializer()
    criterion_achievements = ReportCriterionAchievementListSerializer(many=True)
    class Meta:
        model = ReportExtra
        fields = (
            "id",
            "author",
            "student",
            "period",
            "group",
            "comment",
            "created_at",
            "updated_at",
            "criterion_achievements",
            "role",
            )

# Вывод списка пользователей с фильтрацией репортов службы сопровождения
class UserListReportExtraSerializer(serializers.ModelSerializer):
    short_name = serializers.CharField(source='get_short_name', read_only=True)
    reportextra_student_reports = ReportExtraSerializer(many=True)
    class Meta:
        model = User
        fields = (
            "id", 
            "first_name", 
            "last_name",
            "middle_name",
            "photo",
            "short_name",
            "reportextra_student_reports",
            )
        