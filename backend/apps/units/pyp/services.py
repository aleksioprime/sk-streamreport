from apps.units.pyp.models import (
    PypUnitPlanner,
    TransdisciplinaryTheme,
    PypKeyConcept,
    PypAtlSkill,
    PypLinesOfInquiry,
    PypRelatedConcept,
    PypAtlDevelop,
    PypAtlCluster
    )

def get_pyp_unit_planner_queryset():
    return PypUnitPlanner.objects.select_related(
        'year',
        'transdisciplinary_theme',
        ).prefetch_related(
            'teachers',
            'authors',
            'teacher_roles',
            'ibprofiles',
            'ibprofiles__profile',
            'reflection_posts',
            'reflection_posts__author',
            'key_concepts',
            'inquiry_lines',
            'inquiry_lines__key_concept',
            'related_concepts',
            'atl_develops',
            'atl_develops__skill',
            'atl_develops__skill__group',
            'atl_develops__skill__cluster',
            'atl_develops__skill__cluster__category',
            )

def get_transdisciplinary_theme_queryset():
    return TransdisciplinaryTheme.objects.all()

def get_pyp_key_concept_queryset():
    return PypKeyConcept.objects.all()

def get_pyp_atl_skill_queryset():
    return PypAtlSkill.objects.all().select_related(
        'cluster',
        'cluster__category',
        'group',
        'group__cluster',
        'group__cluster__category',
        )

def get_pyp_atl_cluster_queryset():
    return PypAtlCluster.objects.all().select_related(
        'category',
    )

def get_pyp_lines_inquiry_queryset():
    return PypLinesOfInquiry.objects.all().select_related(
        'key_concept',
        )

def get_pyp_related_concept_queryset():
    return PypRelatedConcept.objects.all()

def get_pyp_atl_develop_queryset():
    return PypAtlDevelop.objects.all().select_related(
        'skill',
        'skill__cluster',
        'skill__cluster__category'
        )