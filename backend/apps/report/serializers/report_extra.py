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
    reports = serializers.SerializerMethodField()
    short_name = serializers.CharField(source='get_short_name', read_only=True)
    class Meta:
        model = User
        fields = (
            "id", 
            "first_name", 
            "last_name",
            "middle_name",
            "reports",
            "photo",
            "short_name",
            )
    def get_reports(self, obj):
        period = self.context['request'].query_params.get('report_period', None)
        group = self.context['request'].query_params.get('report_group', None)
        if period is not None and  group is not None:
            return ReportExtraSerializer(obj.filtered_reports, many=True).data
        else:
            return None
        