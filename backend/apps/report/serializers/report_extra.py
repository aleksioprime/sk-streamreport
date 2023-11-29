from rest_framework import serializers

from apps.report.models import (
    ReportExtra
    )

from .common import (
    UserReportSerializer,
    ClassGroupReportSerializer,
    ReportPeriodListSerializer,
)

from general.models import (
    User
)

# Вывод списка репортов дополнительных сотрудников класса
class ReportExtraListSerializer(serializers.ModelSerializer):
    student = UserReportSerializer()
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

# Подробный просмотр репорта дополнительных сотрудников класса
class ReportExtraRetrieveSerializer(serializers.ModelSerializer):
    student = UserReportSerializer()
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

# Вывод списка пользователей с фильтрацией репортов службы сопровождения
class UserListReportExtraSerializer(serializers.ModelSerializer):
    reportextra_student_reports = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = (
            "id", 
            "first_name", 
            "last_name",
            "middle_name",
            "reportextra_student_reports"
            )
    def get_reportextra_student_reports(self, obj):
        period = self.context['request'].query_params.get('report_period', None)
        group = self.context['request'].query_params.get('report_group', None)
        if period is not None and  group is not None:
            reports = obj.reportextra_student_reports.filter(group=group, period=period)
        else:
            reports = obj.reportextra_student_reports.all()
        return ReportExtraSerializer(reports, many=True).data