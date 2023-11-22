from rest_framework import serializers

from apps.report.models import (
    ReportTeacherPrimary,
    ReportPrimaryTopic,
    ReportTeacherSecondary,
    ReportSecondaryLevel,
    ReportSecondaryCriterion,
    ReportTeacherHigh,
    )

from apps.syllabus.models import (
    CourseTopic
    )

from apps.units.myp.models import (
    MypObjective,
    AchievementLevel
    )

from .common import (
    UserListReportSerializer,
    ClassGroupListReportSerializer,
    ReportPeriodListSerializer,
    SubjectReportListSerializer,
)

# =================  Сериализаторы для репортов учителя НАЧАЛЬНОЙ школы ================= # 

# Список тем курса
class CourseTopicReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseTopic
        fields = (
            "id",
            "section",
            "number",
            "name",
            "description",
            "hours"
            )

# Список достижений по темам предмета для репортов начальной школы
class ReportPrimaryTopicListSerializer(serializers.ModelSerializer):
    topic = CourseTopicReportSerializer()
    class Meta:
        model = ReportPrimaryTopic
        fields = (
            "id",
            "report",
            "topic",
            "level",
            "comment",
            )
        
# Добавление и редактирование достижений по темам предмета
class ReportPrimaryTopicUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportPrimaryTopic
        fields = '__all__'

# Список репортов учителя по предметам начальной школы
class ReportTeacherPrimaryListSerializer(serializers.ModelSerializer):
    student = UserListReportSerializer()
    author = UserListReportSerializer()
    group = ClassGroupListReportSerializer()
    period = ReportPeriodListSerializer()
    subject = SubjectReportListSerializer()
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
            )

# Информация по репорту учителя по предметам начальной школы
class ReportTeacherPrimaryRetrieveSerializer(serializers.ModelSerializer):
    student = UserListReportSerializer()
    author = UserListReportSerializer()
    group = ClassGroupListReportSerializer()
    period = ReportPeriodListSerializer()
    subject = SubjectReportListSerializer()
    topic_achievements = ReportPrimaryTopicListSerializer(many=True)
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
            "topic_achievements",
            "criterion_achievements",
            )

# Создание и обновление репорта учителя по предметам начальной школы
class ReportTeacherPrimaryUpdateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    class Meta:
        model = ReportTeacherPrimary
        fields = '__all__'

# =================  Сериализаторы для репортов учителя СРЕДНЕЙ школы ================= # 

# Список критериев оценки (Objectives)
class MypObjectiveReportListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MypObjective
        fields = (
            "id",
            "letter",
            "name",
            "name_rus",
            "group",
            )

# Список уровней достижений
class AchievementLevelReportListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AchievementLevel
        fields = (
            "id",
            "name",
            "name_rus",
            "strand_level",
            "point",
            )

class ReportSecondaryCriterionListSerializer(serializers.ModelSerializer):
    criterion = MypObjectiveReportListSerializer()
    class Meta:
        model = ReportSecondaryCriterion
        fields = (
            "id",
            "report",
            "criterion",
            "mark"
            )
        
class ReportSecondaryCriterionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportSecondaryCriterion
        fields = '__all__'

class ReportSecondaryLevelListSerializer(serializers.ModelSerializer):
    objective = MypObjectiveReportListSerializer()
    level = AchievementLevelReportListSerializer()
    class Meta:
        model = ReportSecondaryLevel
        fields = (
            "id",
            "report",
            "objective",
            "level",
            )
        
class ReportSecondaryLevelUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportSecondaryLevel
        fields = '__all__'

# Список репортов учителя средней школы
class ReportTeacherSecondaryListSerializer(serializers.ModelSerializer):
    student = UserListReportSerializer()
    author = UserListReportSerializer()
    group = ClassGroupListReportSerializer()
    period = ReportPeriodListSerializer()
    subject = SubjectReportListSerializer()
    class Meta:
        model = ReportTeacherSecondary
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
            )
        
class ReportTeacherSecondaryRetrieveSerializer(serializers.ModelSerializer):
    student = UserListReportSerializer()
    author = UserListReportSerializer()
    group = ClassGroupListReportSerializer()
    period = ReportPeriodListSerializer()
    subject = SubjectReportListSerializer()
    criterion_marks = ReportSecondaryCriterionListSerializer(many=True)
    objective_levels = ReportSecondaryLevelListSerializer(many=True)
    class Meta:
        model = ReportTeacherSecondary
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
            "criterion_marks",
            "objective_levels",
            "criterion_achievements",
            "final_grade",
            )
        
# Создание и обновление репорта учителя по предметам начальной школы
class ReportTeacherSecondaryUpdateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    class Meta:
        model = ReportTeacherSecondary
        fields = '__all__'

# =================  Сериализаторы для репортов учителя СТАРШЕЙ школы ================= # 

class ReportTeacherHighListSerializer(serializers.ModelSerializer):
    student = UserListReportSerializer()
    author = UserListReportSerializer()
    group = ClassGroupListReportSerializer()
    period = ReportPeriodListSerializer()
    subject = SubjectReportListSerializer()
    class Meta:
        model = ReportTeacherHigh
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
            )
        
class ReportTeacherHighRetrieveSerializer(serializers.ModelSerializer):
    student = UserListReportSerializer()
    author = UserListReportSerializer()
    group = ClassGroupListReportSerializer()
    period = ReportPeriodListSerializer()
    subject = SubjectReportListSerializer()
    class Meta:
        model = ReportTeacherHigh
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
            "final_grade",
            "final_grade_ib",
            )
        
class ReportTeacherHighUpdateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    class Meta:
        model = ReportTeacherHigh
        fields = '__all__'