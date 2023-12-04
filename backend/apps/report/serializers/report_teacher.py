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
    StrandLevel,
    StrandLevelAchievement
    )

from .common import (
    UserReportSerializer,
    ClassGroupReportSerializer,
    ReportPeriodListSerializer,
    SubjectReportSerializer,
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

    # Переопределение метода для создания нескольких объектов
    def create(self, validated_data):
        # Проверка, является ли validated_data списком
        if isinstance(validated_data, list):
            objects_to_create = [ReportPrimaryTopic(**item) for item in validated_data]
            return ReportPrimaryTopic.objects.bulk_create(objects_to_create)
        return ReportPrimaryTopic.objects.create(**validated_data)

# Вывод списка репортов учителя по предметам начальной школы
class ReportTeacherPrimaryListSerializer(serializers.ModelSerializer):
    student = UserReportSerializer()
    author = UserReportSerializer()
    group = ClassGroupReportSerializer()
    period = ReportPeriodListSerializer()
    subject = SubjectReportSerializer()
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

# Подробный просмотр репорта учителя по предметам начальной школы
class ReportTeacherPrimaryRetrieveSerializer(serializers.ModelSerializer):
    student = UserReportSerializer()
    author = UserReportSerializer()
    group = ClassGroupReportSerializer()
    period = ReportPeriodListSerializer()
    subject = SubjectReportSerializer()
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

# 
class StrandLevelReportSerializer(serializers.ModelSerializer):
    achieve_levels = StrandLevelAchievementReportListSerializer(many=True)
    strand_letter = serializers.CharField(source='strand.get_letter_display', read_only=True)
    objective = serializers.CharField(source='strand.objective.id', read_only=True)
    objective_letter = serializers.CharField(source='strand.objective.letter', read_only=True)
    class Meta:
        model = StrandLevel
        fields = (
            "id",
            "name",
            "name_rus",
            "level",
            "objective",
            "achieve_levels",
            "objective_letter",
            "strand_letter",
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
    strand = StrandLevelReportSerializer()
    level = StrandLevelAchievementReportListSerializer()
    class Meta:
        model = ReportSecondaryLevel
        fields = (
            "id",
            "report",
            "strand",
            "level",
            )
        
# Создание и редактирование достижения по предметным целям MYP для репорта учителя по предметам средней школы
class ReportSecondaryLevelUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportSecondaryLevel
        fields = '__all__'

# Вывод списка репортов учителя по предметам средней школы
class ReportTeacherSecondaryListSerializer(serializers.ModelSerializer):
    student = UserReportSerializer()
    author = UserReportSerializer()
    group = ClassGroupReportSerializer()
    period = ReportPeriodListSerializer()
    subject = SubjectReportSerializer()
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

# Подробный просмотр репорта учителя по предметам средней школы    
class ReportTeacherSecondaryRetrieveSerializer(serializers.ModelSerializer):
    student = UserReportSerializer()
    author = UserReportSerializer()
    group = ClassGroupReportSerializer()
    period = ReportPeriodListSerializer()
    subject = SubjectReportSerializer()
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
    student = UserReportSerializer()
    author = UserReportSerializer()
    group = ClassGroupReportSerializer()
    period = ReportPeriodListSerializer()
    subject = SubjectReportSerializer()
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

# Подробный просмотр репорта учителя по предметам старшей школы  
class ReportTeacherHighRetrieveSerializer(serializers.ModelSerializer):
    student = UserReportSerializer()
    author = UserReportSerializer()
    group = ClassGroupReportSerializer()
    period = ReportPeriodListSerializer()
    subject = SubjectReportSerializer()
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