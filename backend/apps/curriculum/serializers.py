from rest_framework import serializers

from apps.curriculum.models import (
    FgosSubjectGroup,
    IbSubjectGroup,
    IbDiscipline,
    Subject,
    Curriculum,
    CurriculumLoad,
    TeachingLoad,
    )

from general.models import (
    User,
    StudyYear,
    AcademicYear,
    ClassGroup,
    )


class FgosSubjectGroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FgosSubjectGroup
        fields = (
            "id",
            "name",
            "type",
            )
        
class IbSubjectGroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = IbSubjectGroup
        fields = (
            "id",
            "name",
            "name_rus",
            "logo",
            "program"
            )

# Список предметов
class SubjectListSerializer(serializers.ModelSerializer):
    group_ib = IbSubjectGroupListSerializer()
    group_fgos = FgosSubjectGroupListSerializer()
    class Meta:
        model = Subject
        fields = (
            "id",
            "name",
            "name_eng",
            "group_ib",
            "group_fgos",
            "type",
            "dnevnik_id",
            "department",
            "level",
            "need_report"
            )
        
class CurriculumListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = (
            "id",
            "year",
            "name",
            "name_short",
            "level"
            )
        
class StudyYearListCurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyYear
        fields = (
            "id",
            "number",
            "level",
            )
        
# Нагрузка учебных планов
class CurriculumLoadListSerializer(serializers.ModelSerializer):
    curriculum = CurriculumListSerializer()
    subject = SubjectListSerializer()
    years = StudyYearListCurriculumSerializer(many=True)
    class Meta:
        model = CurriculumLoad
        fields = (
            "id",
            "curriculum",
            "subject",
            "years",
            "hours"
            )

class AcademicYearListCurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = (
            "id",
            "name",
            "date_start",
            "date_end"
            )
        
class UserListCurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id", 
            "first_name", 
            "last_name",
            "middle_name",
            "email",
            "dnevnik_id",
            )

class ClassGroupListCurriculumSerializer(serializers.ModelSerializer):
    year_academic = AcademicYearListCurriculumSerializer()
    year_study = StudyYearListCurriculumSerializer()
    class Meta:
        model = ClassGroup
        fields = (
            "id",
            "year_academic",
            "year_study",
            "letter",
            )

# Преподавательская нагрузка
class TeachingLoadListSerializer(serializers.ModelSerializer):
    year = AcademicYearListCurriculumSerializer()
    teacher = UserListCurriculumSerializer()
    subject = SubjectListSerializer()
    groups = ClassGroupListCurriculumSerializer(many=True)
    class Meta:
        model = TeachingLoad
        fields = (
            "id",
            "year",
            "teacher",
            "subject",
            "groups",
            "hours"
            )