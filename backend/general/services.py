from general.models import (
    User,
    ClassGroup,
    AcademicYear,
    StudyYear
)

def get_user_queryset():
    return User.objects.prefetch_related(
            "groups",
            "departments",
            "group_roles__group",
            "group_roles__group__year_study",
            "mentor_classes",
            "teaching_loads",
            "teaching_loads__groups__year_study",
            "teaching_loads__subject",
            "teaching_loads__year",
        )

def get_group_queryset():
    return ClassGroup.objects.all().select_related(
            "year_academic",
            "year_study",
            "year_study__ib",
            "mentor",
            "curriculum",
        )

def load_file_excel():
    pass

def get_academic_year_queryset():
    return AcademicYear.objects.all()

def get_study_year_queryset():
    return StudyYear.objects.all().select_related(
            "ib",
        )