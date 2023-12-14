from rest_framework import serializers

from apps.report.models import (
    ReportMentor,
    ReportIbProfile,
    ReportMentorPrimary,
    ReportPrimaryUnit,
    ReportExtra,
    ReportTeacherPrimary,
    ReportCriterionAchievement,
    ReportSecondaryCriterion,
    ReportSecondaryLevel
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
    EventParticipationReportSerializer,
    StudentReportSerializer,
    ReportCriterionLevelSerializer,
    ReportCriterionListSerializer,
    StudyYearReportSerializer
)

from .report_teacher import (
    ReportTeacherPrimaryListSerializer,
    ReportTeacherSecondaryListSerializer,
    ReportTeacherHighListSerializer,
    SubjectReportSerializer,
    ReportPrimaryTopicListSerializer,
    ReportCriterionAchievementListSerializer
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
    student = StudentReportSerializer()
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
    student = StudentReportSerializer()
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
    teachers = UserReportSerializer(many=True)
    year = StudyYearReportSerializer()
    class Meta:
        model = PypUnitPlanner
        fields = (
            "id",
            "title",
            "teachers",
            "year",
            "transdisciplinary_theme",
            "central_idea",
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
    student = StudentReportSerializer()
    author = UserReportSerializer()
    group = ClassGroupReportSerializer()
    period = ReportPeriodListSerializer()
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
            "pyp_units",
            "created_at",
            "updated_at",
            )

# Подробный просмотр репорта классного руководителя начальной школы
class ReportMentorPrimaryRetrieveSerializer(serializers.ModelSerializer):
    student = StudentReportSerializer()
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
        


# ******************* Сериализаторы списка студентов в репортах наставника *****************

class ReportMentorSerializer(serializers.ModelSerializer):
    author = UserReportSerializer()
    student = StudentReportSerializer()
    profiles = ReportIbProfileListSerializer(many=True)
    group = ClassGroupReportSerializer()
    pyp_units = serializers.SerializerMethodField()
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
            "pyp_units",
            "created_at",
            "updated_at",
            )
    def get_pyp_units(self, obj):
        if hasattr(obj, 'reportmentorprimary'):
            return ReportPrimaryUnitListSerializer(obj.reportmentorprimary.pyp_units, many=True).data
        return None
        

# Вывод списка репортов дополнительных сотрудников класса
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
        
# Вывод списка достижений по критериям для репортов учителя
class ReportCriterionAchievementSerializer(serializers.ModelSerializer):
    criterion_name = serializers.CharField(source='criterion.name', read_only=True)
    achievement_name = serializers.CharField(source='achievement.name', read_only=True)
    class Meta:
        model = ReportCriterionAchievement
        fields = (
            'criterion_name',
            'achievement_name',
            'id',
            'report'
        )

class ReportSecondaryCriterionSerializer(serializers.ModelSerializer):
    criterion_name = serializers.CharField(source='criterion.name', read_only=True)
    class Meta:
        model = ReportSecondaryCriterion
        fields = (
            "id",
            "report",
            "criterion_name",
            "mark"
            )

class ReportSecondaryLevelSerializer(serializers.ModelSerializer):
    level_name = serializers.CharField(source='level.name', read_only=True)
    strand_name = serializers.CharField(source='strand.name', read_only=True)
    class Meta:
        model = ReportSecondaryLevel
        fields = (
            "id",
            "report",
            "level_name",
            "strand_name",
            )

class ReportTeacherSerializer(serializers.ModelSerializer):
    author = UserReportSerializer()
    subject = SubjectReportSerializer()
    criterion_achievements = ReportCriterionAchievementSerializer(many=True)
    class Meta:
        model = ReportTeacherPrimary
        fields = (
            "id",
            "student",
            "author",
            "period",
            "group",
            "subject",
            "comment",
            "created_at",
            "updated_at",
            'criterion_achievements'
            )

class ReportTeacherPrimarySerializer(ReportTeacherSerializer):
    topic_achievements = ReportPrimaryTopicListSerializer(many=True)
    class Meta(ReportTeacherSerializer.Meta):
        fields = ReportTeacherSerializer.Meta.fields + (
            'topic_achievements',
            )
        
class ReportTeacherSecondarySerializer(ReportTeacherSerializer):
    criterion_marks = ReportSecondaryCriterionSerializer(many=True)
    objective_levels = ReportSecondaryLevelSerializer(many=True)
    class Meta(ReportTeacherSerializer.Meta):
        fields = ReportTeacherSerializer.Meta.fields + (
            'criterion_marks',
            'objective_levels'
            )
class ReportTeacherHighSerializer(ReportTeacherSerializer):
    class Meta(ReportTeacherSerializer.Meta):
        fields = ReportTeacherSerializer.Meta.fields

# Вывод списка пользователей с фильтрацией репортов классных руководителей
class UserListReportMentorSerializer(serializers.ModelSerializer):
    teacher_primary_reports = serializers.SerializerMethodField()
    teacher_secondary_reports = serializers.SerializerMethodField()
    teacher_high_reports = serializers.SerializerMethodField()
    short_name = serializers.CharField(source='get_short_name', read_only=True)
    reportmentor_student_reports = ReportMentorSerializer(many=True)
    reportextra_student_reports = ReportExtraSerializer(many=True)
    class Meta:
        model = User
        fields = (
            "id", 
            "first_name", 
            "last_name",
            "middle_name",
            "short_name",
            "teacher_primary_reports",
            "teacher_secondary_reports",
            "teacher_high_reports",
            "photo",
            "reportmentor_student_reports",
            "reportextra_student_reports",
            )
    def get_teacher_primary_reports(self, obj):
        period = self.context['request'].query_params.get('report_period', None)
        group = self.context['request'].query_params.get('report_group', None)
        if period is not None and  group is not None:
            return ReportTeacherPrimarySerializer(obj.filtered_teacher_primary_reports, many=True).data
        else:
            return []
    def get_teacher_secondary_reports(self, obj):
        period = self.context['request'].query_params.get('report_period', None)
        group = self.context['request'].query_params.get('report_group', None)
        if period is not None and  group is not None:
            return ReportTeacherSecondarySerializer(obj.filtered_teacher_secondary_reports, many=True).data
        else:
            return []
    def get_teacher_high_reports(self, obj):
        period = self.context['request'].query_params.get('report_period', None)
        group = self.context['request'].query_params.get('report_group', None)
        if period is not None and  group is not None:
            return ReportTeacherHighSerializer(obj.filtered_teacher_high_reports, many=True).data
        else:
            return []