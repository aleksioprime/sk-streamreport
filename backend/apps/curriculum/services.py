from apps.curriculum.models import (
    Subject,
    Curriculum,
    CurriculumLoad,
    TeachingLoad,
)

def get_subject_queryset():
    return Subject.objects.all().select_related(
        'group_ib',
        'group_fgos',
        'discipline_ib',
        'department'
    )

def get_curriculum_queryset():
    return Curriculum.objects.all().select_related(
        'year',
    )

def get_curriculum_load_queryset():
    return CurriculumLoad.objects.all().select_related(
        'subject',
    ).prefetch_related(
        'years'
        )

def get_teaching_load_queryset():
    return TeachingLoad.objects.all().select_related(
        'year',
        'teacher',
        'subject',
    ).prefetch_related(
        'groups'
    )