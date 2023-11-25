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
    StrandLevelAchievement
    )

from .common import (
    UserListReportSerializer,
    ClassGroupListReportSerializer,
    ReportPeriodListSerializer,
    SubjectReportListSerializer,
    ReportCriterionAchievementListSerializer,
)

# =================  Сериализаторы для репортов учителя НАЧАЛЬНОЙ школы ================= # 

# Список тем курса (и секций курса)
class CourseTopicReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseTopic
        fields = (
            "id",
            "chapter",
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

# Вывод списка репортов учителя по предметам начальной школы
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

# Подробный просмотр репорта учителя по предметам начальной школы
class ReportTeacherPrimaryRetrieveSerializer(serializers.ModelSerializer):
    student = UserListReportSerializer()
    author = UserListReportSerializer()
    group = ClassGroupListReportSerializer()
    period = ReportPeriodListSerializer()
    subject = SubjectReportListSerializer()
    topic_achievements = ReportPrimaryTopicListSerializer(many=True)
    criterion_achievements = ReportCriterionAchievementListSerializer(many=True)
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

# Создание и редактирование репорта учителя по предметам начальной школы
class ReportTeacherPrimaryUpdateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    class Meta:
        model = ReportTeacherPrimary
        fields = '__all__'

# =================  Сериализаторы для репортов учителя СРЕДНЕЙ школы ================= # 

# Список критериев оценки (Objectives) MYP
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

# Список уровней достижений MYP
class StrandLevelAchievementReportListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrandLevelAchievement
        fields = (
            "id",
            "name",
            "name_rus",
            "level",
            "point",
            )

# Вывод списка баллов по критериям оценки MYP для репорта учителя по предметам средней школы
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

# Создание и редактирование балла по критерию оценки MYP для репорта учителя по предметам средней школы
class ReportSecondaryCriterionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportSecondaryCriterion
        fields = '__all__'

# Вывод списка достижений по предметным целям MYP для репорта учителя по предметам средней школы
class ReportSecondaryLevelListSerializer(serializers.ModelSerializer):
    objective = MypObjectiveReportListSerializer()
    level = StrandLevelAchievementReportListSerializer()
    class Meta:
        model = ReportSecondaryLevel
        fields = (
            "id",
            "report",
            "objective",
            "level",
            )
        
# Создание и редактирование достижения по предметным целям MYP для репорта учителя по предметам средней школы
class ReportSecondaryLevelUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportSecondaryLevel
        fields = '__all__'

# Вывод списка репортов учителя по предметам средней школы
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

# Подробный просмотр репорта учителя по предметам средней школы    
class ReportTeacherSecondaryRetrieveSerializer(serializers.ModelSerializer):
    student = UserListReportSerializer()
    author = UserListReportSerializer()
    group = ClassGroupListReportSerializer()
    period = ReportPeriodListSerializer()
    subject = SubjectReportListSerializer()
    criterion_marks = ReportSecondaryCriterionListSerializer(many=True)
    objective_levels = ReportSecondaryLevelListSerializer(many=True)
    criterion_achievements = ReportCriterionAchievementListSerializer(many=True)
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
        
# Создание и редактирование репорта учителя по предметам средней школы
class ReportTeacherSecondaryUpdateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    class Meta:
        model = ReportTeacherSecondary
        fields = '__all__'

# =================  Сериализаторы для репортов учителя СТАРШЕЙ школы ================= # 

# Вывод списка репортов учителя по предметам старшей школы
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

# Подробный просмотр репорта учителя по предметам старшей школы  
class ReportTeacherHighRetrieveSerializer(serializers.ModelSerializer):
    student = UserListReportSerializer()
    author = UserListReportSerializer()
    group = ClassGroupListReportSerializer()
    period = ReportPeriodListSerializer()
    subject = SubjectReportListSerializer()
    criterion_achievements = ReportCriterionAchievementListSerializer(many=True)
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
            "criterion_achievements",
            "final_grade",
            "final_grade_ib",
            )

# Создание и редактирование репорта учителя по предметам старшей школы
class ReportTeacherHighUpdateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    class Meta:
        model = ReportTeacherHigh
        fields = '__all__'