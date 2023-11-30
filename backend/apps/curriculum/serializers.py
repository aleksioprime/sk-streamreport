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
    Department,
    )

# Cписок предметных групп по ФГОС
class FgosSubjectGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = FgosSubjectGroup
        fields = (
            "id",
            "name",
            "type",
            )

# Cписок предметных групп по IB
class IbSubjectGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = IbSubjectGroup
        fields = (
            "id",
            "name",
            "name_rus",
            "logo",
            "program"
            )
        
# Cписок подразделений
class DepartmentCurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = (
            "id",
            "name",
            "logo",
            )

# Вывод списка предметов
class SubjectListSerializer(serializers.ModelSerializer):
    group_ib = IbSubjectGroupSerializer()
    group_fgos = FgosSubjectGroupSerializer()
    department = DepartmentCurriculumSerializer()
    class Meta:
        model = Subject
        fields = (
            "id",
            "name",
            "name_eng",
            "group_ib",
            "group_fgos",
            "dnevnik_id",
            "department",
            "level",
            "need_report"
            )

# Вывод списка учебных планов
class CurriculumListSerializer(serializers.ModelSerializer):
    level_name = serializers.CharField(source='get_level_display', read_only=True)
    class Meta:
        model = Curriculum
        fields = (
            "id",
            "year",
            "name",
            "name_short",
            "level",
            "level_name",
            "ib",
            )

# Список параллелей обучения
class StudyYearCurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyYear
        fields = (
            "id",
            "number",
            "level",
            )
        
# Вывод списка нагрузки учебных планов
class CurriculumLoadListSerializer(serializers.ModelSerializer):
    curriculum = CurriculumListSerializer()
    subject = SubjectListSerializer()
    years = StudyYearCurriculumSerializer(many=True)
    class Meta:
        model = CurriculumLoad
        fields = (
            "id",
            "curriculum",
            "subject",
            "years",
            "hours"
            )

# Нагрузка учебных планов (дополнительный сериализатор)
class CurriculumLoadSerializer(serializers.ModelSerializer):
    subject = SubjectListSerializer()
    years = StudyYearCurriculumSerializer(many=True)
    class Meta:
        model = CurriculumLoad
        fields = (
            "id",
            "subject",
            "years",
            "hours"
            )

# Подробный просмотр учебного плана
class CurriculumRetrieveSerializer(serializers.ModelSerializer):
    curriculum_loads = CurriculumLoadSerializer(many=True)
    class Meta:
        model = Curriculum
        fields = (
            "id",
            "year",
            "name",
            "name_short",
            "level",
            "curriculum_loads"
            )

# Список учебных лет
class AcademicYearCurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = (
            "id",
            "name",
            "date_start",
            "date_end"
            )

# Список пользователей
class UserCurriculumSerializer(serializers.ModelSerializer):
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

# Список учебных классов
class ClassGroupListCurriculumSerializer(serializers.ModelSerializer):
    year_academic = AcademicYearCurriculumSerializer()
    year_study = StudyYearCurriculumSerializer()
    class Meta:
        model = ClassGroup
        fields = (
            "id",
            "year_academic",
            "year_study",
            "letter",
            )

# Вывод списка преподавательской нагрузки
class TeachingLoadListSerializer(serializers.ModelSerializer):
    year = AcademicYearCurriculumSerializer()
    teacher = UserCurriculumSerializer()
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