from apps.units.pyp.models import (
    PypUnitPlanner,
    TransdisciplinaryTheme,
    PypKeyConcept,
    PypAtlSkill,
    PypLinesOfInquiry,
    PypRelatedConcept,
    PypAtlDevelop
    )

def get_pyp_unit_planner_queryset():
    return PypUnitPlanner.objects.all().select_related(
        'year'
        'transdisciplinary_theme',
        ).prefetch_related(
            'teachers',
            'authors',
            'teacher_roles',
            'ibprofiles',
            'reflection_posts',
            'key_concepts',
            'inquiry_lines',
            'related_concepts',
            'atl_develops'
            )

def get_transdisciplinary_theme_queryset():
    return TransdisciplinaryTheme.objects.all()

def get_pyp_key_concept_queryset():
    return PypKeyConcept.objects.all()

def get_pyp_atl_skill_queryset():
    return PypAtlSkill.objects.all().select_related(
        'cluster',
        'group',
        )

def get_pyp_lines_inquiry_queryset():
    return PypLinesOfInquiry.objects.all().select_related(
        'key_concept',
        )

def get_pyp_related_concept_queryset():
    return PypRelatedConcept.objects.all()

def get_pyp_atl_develop_queryset():
    return PypAtlDevelop.objects.all().select_related(
        'atl',
        )