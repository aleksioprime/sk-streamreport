from general.models import (
    User,
    ClassGroup,
    AcademicYear,
    StudyYear
)

def get_user_queryset():
    return User.objects.all().prefetch_related(
            "groups",
            "departments",
            "group_roles",
            "mentor_classes",
            "mentor_classes__year",
            "teaching_loads",
            "teaching_loads__groups",
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