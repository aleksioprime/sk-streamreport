from apps.curriculum.models import (
    Subject,
    CurriculumLoad,
    TeachingLoad,
)

def get_subject_queryset():
    return Subject.objects.all().order_by("name")

def get_curriculum_load_queryset():
    return CurriculumLoad.objects.all().order_by("curriculum", "subject")

def get_teaching_load_queryset():
    return TeachingLoad.objects.all().order_by("year", "teacher")