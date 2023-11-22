from rest_framework import serializers

from apps.report.models import (
    ReportMentor,
    ReportIbProfile,
    ReportMentorPrimary,
    ReportPrimaryUnit,
    )

from .common import (
    UserListReportSerializer,
    ClassGroupListReportSerializer,
    ReportPeriodListSerializer,
)

# Список уровня развития профиля студента IB для репортов классного руководителя
class ReportIbProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportIbProfile
        fields = (
            "id",
            "report",
            "profile",
            "level"
            )

# Список репортов классного руководителя
class ReportMentorListSerializer(serializers.ModelSerializer):
    student = UserListReportSerializer()
    author = UserListReportSerializer()
    group = ClassGroupListReportSerializer()
    period = ReportPeriodListSerializer()
    class Meta:
        model = ReportMentor
        fields = (
            "id",
            "student",
            "author",
            "period",
            "group",
            "comment",
            "created_at",
            "updated_at",
            )

# Список юнитов для репорта классного руководителя начальной школы
class ReportPrimaryUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportPrimaryUnit
        fields = (
            "id",
            "report",
            "unit",
            "comment"
            )
        
# Список репортов классного руководителя начальной школы
class ReportMentorPrimaryListSerializer(serializers.ModelSerializer):
    student = UserListReportSerializer()
    author = UserListReportSerializer()
    group = ClassGroupListReportSerializer()
    period = ReportPeriodListSerializer()
    class Meta:
        model = ReportMentorPrimary
        fields = (
            "id",
            "student",
            "author",
            "period",
            "group",
            "comment",
            "created_at",
            "updated_at",
            )
            