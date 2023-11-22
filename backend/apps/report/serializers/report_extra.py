from rest_framework import serializers

from apps.report.models import (
    ReportExtra
    )

from .common import (
    UserListReportSerializer,
    ClassGroupListReportSerializer,
    ReportPeriodListSerializer,
)

class ReportExtraListSerializer(serializers.ModelSerializer):
    student = UserListReportSerializer()
    author = UserListReportSerializer()
    group = ClassGroupListReportSerializer()
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