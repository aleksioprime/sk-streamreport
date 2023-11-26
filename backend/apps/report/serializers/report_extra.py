from rest_framework import serializers

from apps.report.models import (
    ReportExtra
    )

from .common import (
    UserReportSerializer,
    ClassGroupReportSerializer,
    ReportPeriodListSerializer,
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