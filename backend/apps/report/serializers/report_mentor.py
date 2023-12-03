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

from .report_teacher import (
    ReportTeacherPrimaryListSerializer,
    ReportTeacherSecondaryListSerializer,
    ReportTeacherHighListSerializer,
)

from .report_extra import (
    ReportExtraListSerializer
)

from general.models import (
    User
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



class ReportMentorPrimarySerializer(serializers.ModelSerializer):
    author = UserReportSerializer()
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

# Вывод списка пользователей с фильтрацией репортов классных руководителей
class UserListReportMentorPrimarySerializer(serializers.ModelSerializer):
    reports = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = (
            "id", 
            "first_name", 
            "last_name",
            "middle_name",
            "reports",
            "photo",
            )
    def get_reports(self, obj):
        period = self.context['request'].query_params.get('report_period', None)
        group = self.context['request'].query_params.get('report_group', None)
        if period is not None and  group is not None:
            return ReportMentorPrimarySerializer(obj.filtered_reports, many=True).data
        else:
            return None
        

class ReportMentorSerializer(serializers.ModelSerializer):
    author = UserReportSerializer()
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

# Вывод списка пользователей с фильтрацией репортов классных руководителей
class UserListReportMentorSerializer(serializers.ModelSerializer):
    reports = serializers.SerializerMethodField()
    teacher_primary_reports = serializers.SerializerMethodField()
    teacher_secondary_reports = serializers.SerializerMethodField()
    teacher_high_reports = serializers.SerializerMethodField()
    extra_reports = serializers.SerializerMethodField()
    short_name = serializers.CharField(source='get_short_name', read_only=True)
    class Meta:
        model = User
        fields = (
            "id", 
            "first_name", 
            "last_name",
            "middle_name",
            "short_name",
            "reports",
            "teacher_primary_reports",
            "teacher_secondary_reports",
            "teacher_high_reports",
            "extra_reports",
            "photo",
            )
    def get_reports(self, obj):
        period = self.context['request'].query_params.get('report_period', None)
        group = self.context['request'].query_params.get('report_group', None)
        if period is not None and  group is not None:
            return ReportMentorSerializer(obj.filtered_reports, many=True).data
        else:
            return None
    def get_teacher_primary_reports(self, obj):
        period = self.context['request'].query_params.get('report_period', None)
        group = self.context['request'].query_params.get('report_group', None)
        if period is not None and  group is not None:
            return ReportTeacherPrimaryListSerializer(obj.filtered_teacher_primary_reports, many=True).data
        else:
            return None
    def get_teacher_secondary_reports(self, obj):
        period = self.context['request'].query_params.get('report_period', None)
        group = self.context['request'].query_params.get('report_group', None)
        if period is not None and  group is not None:
            return ReportTeacherSecondaryListSerializer(obj.filtered_teacher_secondary_reports, many=True).data
        else:
            return None
    def get_teacher_high_reports(self, obj):
        period = self.context['request'].query_params.get('report_period', None)
        group = self.context['request'].query_params.get('report_group', None)
        if period is not None and  group is not None:
            return ReportTeacherHighListSerializer(obj.filtered_teacher_high_reports, many=True).data
        else:
            return None
    def get_extra_reports(self, obj):
        period = self.context['request'].query_params.get('report_period', None)
        group = self.context['request'].query_params.get('report_group', None)
        if period is not None and  group is not None:
            return ReportExtraListSerializer(obj.filtered_extra_reports, many=True).data
        else:
            return None