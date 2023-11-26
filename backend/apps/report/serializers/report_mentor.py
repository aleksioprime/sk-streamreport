from rest_framework import serializers

from apps.report.models import (
    ReportMentor,
    ReportIbProfile,
    ReportMentorPrimary,
    ReportPrimaryUnit,
    )

from apps.ibo.models import (
    LearnerProfile,
)

from apps.units.pyp.models import (
    PypUnitPlanner
)

from .common import (
    UserReportSerializer,
    ClassGroupReportSerializer,
    ReportPeriodListSerializer,
)

# Список профилей студента IB
class LearnerProfileReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearnerProfile
        fields = (
            "id",
            "name",
            "name_rus",
            )

# Вывод списка уровней развития профиля студента IB для репортов классного руководителя
class ReportIbProfileListSerializer(serializers.ModelSerializer):
    profile = LearnerProfileReportSerializer()
    class Meta:
        model = ReportIbProfile
        fields = (
            "id",
            "report",
            "profile",
            "level"
            )

# Создание и редактирование уровня развития профиля студента IB для репортов классного руководителя
class ReportIbProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportIbProfile
        fields = '__all__'

# Вывод списка репортов классного руководителя
class ReportMentorListSerializer(serializers.ModelSerializer):
    student = UserReportSerializer()
    author = UserReportSerializer()
    group = ClassGroupReportSerializer()
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
        
# Подробный просмотр репорта классного руководителя
class ReportMentorRetrieveSerializer(serializers.ModelSerializer):
    student = UserReportSerializer()
    author = UserReportSerializer()
    group = ClassGroupReportSerializer()
    period = ReportPeriodListSerializer()
    profiles = ReportIbProfileListSerializer(many=True)
    class Meta:
        model = ReportMentor
        fields = (
            "id",
            "student",
            "author",
            "period",
            "group",
            "comment",
            "profiles",
            "created_at",
            "updated_at",
            )

# Создание и редактирование репорта классного руководителя
class ReportMentorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportMentor
        fields = '__all__'

# TODO: Добавить необходимые поля для отображения
# Список UnitPlanner начальной школы (PYP)
class PypUnitPlannerReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = PypUnitPlanner
        fields = (
            "id",
            "title",
            "transdisciplinary_theme",
            "central_idea"
            )

# Список результатов юнитов для репорта классного руководителя начальной школы
class ReportPrimaryUnitListSerializer(serializers.ModelSerializer):
    unit = PypUnitPlannerReportSerializer()
    class Meta:
        model = ReportPrimaryUnit
        fields = (
            "id",
            "report",
            "unit",
            "comment"
            )

# Создание и редактирование результатов юнитов для репорта классного руководителя начальной школы
class ReportPrimaryUnitUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportPrimaryUnit
        fields = '__all__'
        
# Список репортов классного руководителя начальной школы
class ReportMentorPrimaryListSerializer(serializers.ModelSerializer):
    student = UserReportSerializer()
    author = UserReportSerializer()
    group = ClassGroupReportSerializer()
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

# Подробный просмотр репорта классного руководителя начальной школы
class ReportMentorPrimaryRetrieveSerializer(serializers.ModelSerializer):
    student = UserReportSerializer()
    author = UserReportSerializer()
    group = ClassGroupReportSerializer()
    period = ReportPeriodListSerializer()
    profiles = ReportIbProfileListSerializer(many=True)
    pyp_units = ReportPrimaryUnitListSerializer(many=True)
    class Meta:
        model = ReportMentorPrimary
        fields = (
            "id",
            "student",
            "author",
            "period",
            "group",
            "comment",
            "profiles",
            "pyp_units",
            "created_at",
            "updated_at",
            )

# Создание и редактирование репорта классного руководителя начальной школы
class ReportMentorPrimaryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportMentorPrimary
        fields = '__all__'