from rest_framework import serializers
from django.db.models import Q

from apps.report.models import (
    ReportPeriod,
    ReportTeacherPrimary,
    ReportPrimaryUnit,
    ReportIbProfile,
    ReportPrimaryAchievement,
    ReportTeacherSecondary,
    ReportSecondaryCriterion,
    ReportTeacherHigh,
    ReportMentor,
    ReportExtra
    )

from general.models import (
    User,
    AcademicYear,
    ClassGroup,
    StudyYear,
    )

from apps.curriculum.models import (
    Subject
    )

from apps.syllabus.models import (
    CourseTopic
    )

from apps.units.myp.models import (
    MypObjective,
    AchievementLevel
    )


class UserListReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id", 
            "first_name", 
            "last_name",
            "middle_name",
            )

class AcademicYearListReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = (
            "id",
            "name",
            "date_start",
            "date_end"
            )
        
class StudyYearListReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyYear
        fields = (
            "id",
            "number",
            "level",
            )

class ClassGroupListReportSerializer(serializers.ModelSerializer):
    year_academic = AcademicYearListReportSerializer()
    year_study = StudyYearListReportSerializer()
    class Meta:
        model = ClassGroup
        fields = (
            "id",
            "year_academic",
            "year_study",
            "letter",
            )

class ReportPeriodListReportSerializer(serializers.ModelSerializer):
    year = AcademicYearListReportSerializer()
    class Meta:
        model = ReportPeriod
        fields = (
            "id",
            "order",
            "name",
            "year",
            "date_start",
            "date_end",
            )

class SubjectReportListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = (
            "id", 
            "name", 
            "name_eng",
            "type",
            "level",
            "need_report"
            )

# =================  Сериализаторы для репортов учителя НАЧАЛЬНОЙ школы ================= # 

# Список уровня развития профиля студента IB для репортов начальной школы
class ReportIbProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportIbProfile
        fields = (
            "id",
            "report",
            "profile",
            "level"
            )

# Список тем по предмету
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
class ReportPrimaryAchievementSerializer(serializers.ModelSerializer):
    topic = CourseTopicReportSerializer()
    class Meta:
        model = ReportPrimaryAchievement
        fields = (
            "id",
            "report",
            "topic",
            "level",
            "comment",
            )

# Список юнитов для репорта начальной школы
class ReportPrimaryUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportPrimaryUnit
        fields = (
            "id",
            "report",
            "unit",
            "comment"
            )

# Список репортов учителя по предметам начальной школы
class ReportTeacherPrimaryListSerializer(serializers.ModelSerializer):
    student = UserListReportSerializer()
    author = UserListReportSerializer()
    group = ClassGroupListReportSerializer()
    period = ReportPeriodListReportSerializer()
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
    period = ReportPeriodListReportSerializer()
    subject = SubjectReportListSerializer()
    units = ReportPrimaryUnitSerializer(many=True)
    profiles = ReportIbProfileSerializer(many=True)
    achievements = ReportPrimaryAchievementSerializer(many=True)
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
            "units",
            "profiles",
            "achievements",
            )

# Создание и обновление репорта учителя по предметам начальной школы
class ReportTeacherPrimaryCreateUpdateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    units = ReportPrimaryUnitSerializer(many=True, required=False)
    profiles = ReportIbProfileSerializer(many=True, required=False)
    achievements = ReportPrimaryAchievementSerializer(many=True, required=False)
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
            "units",
            "profiles",
            "achievements",
            )
    
    def create_or_update_related_field(self, related_field, model_class):
        related_fields_ids = []
        for field in related_field:
            field_instance, created = model_class.objects.update_or_create(pk=field.get('id'), defaults=field)
            related_fields_ids.append(field_instance.pk)
        return related_fields_ids
    
    def update(self, instance, validated_data):
        print('Валидированные данные: ', validated_data)
        units = validated_data.pop('units', None)
        if units is not None:
            instance_units = ReportPrimaryUnitSerializer.objects.filter(report=instance)
            instance_units.filter(~Q(id__in=[item.get('id') for item in units if 'id' in item])).delete()
            instance.events.set(self.create_or_update_related_field(units, ReportPrimaryUnitSerializer))
            instance.save()
        profiles = validated_data.pop('profiles', None)
        if profiles is not None:
            instance_profiles = ReportIbProfileSerializer.objects.filter(report=instance)
            instance_profiles.filter(~Q(id__in=[item.get('id') for item in profiles if 'id' in item])).delete()
            instance.achievements.set(self.create_or_update_related_field(profiles, ReportIbProfileSerializer))
            instance.save()
        achievements = validated_data.pop('achievements', None)
        if achievements is not None:
            instance_achievements = ReportPrimaryAchievementSerializer.objects.filter(report=instance)
            instance_achievements.filter(~Q(id__in=[item.get('id') for item in achievements if 'id' in item])).delete()  
            instance.achievements.set(self.create_or_update_related_field(achievements, ReportPrimaryAchievementSerializer))
            instance.save()
        return super().update(instance, validated_data)

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

# Список репортов учителя средней школы
class ReportTeacherSecondaryListSerializer(serializers.ModelSerializer):
    student = UserListReportSerializer()
    author = UserListReportSerializer()
    group = ClassGroupListReportSerializer()
    period = ReportPeriodListReportSerializer()
    subject = SubjectReportListSerializer()
    criteria = MypObjectiveReportListSerializer(many=True)
    achievements = AchievementLevelReportListSerializer(many=True)
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
            "criteria",
            "achievements",
            "final_grade",
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

# =================  Сериализаторы для репортов учителя СТАРШЕЙ школы ================= # 

class ReportTeacherHighListSerializer(serializers.ModelSerializer):
    student = UserListReportSerializer()
    author = UserListReportSerializer()
    group = ClassGroupListReportSerializer()
    period = ReportPeriodListReportSerializer()
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

# =================  Сериализаторы для репортов КЛАССНОГО РУКОВОДИТЕЛЯ ================= # 

class ReportMentorListSerializer(serializers.ModelSerializer):
    student = UserListReportSerializer()
    author = UserListReportSerializer()
    group = ClassGroupListReportSerializer()
    period = ReportPeriodListReportSerializer()
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

# =================  Сериализаторы для репортов СОТРУДНИКОВ КЛАССА ================= # 

class ReportExtraListSerializer(serializers.ModelSerializer):
    student = UserListReportSerializer()
    author = UserListReportSerializer()
    group = ClassGroupListReportSerializer()
    period = ReportPeriodListReportSerializer()
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