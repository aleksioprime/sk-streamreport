from apps.units.myp.models import (
    MypUnitPlanner,
    MypUnitPlannerId,
    MypObjective,
    Strand,
    StrandLevel,
    StrandLevelAchievement,
    MypAim,
    MypKeyConcept,
    MypRelatedConcept,
    GlobalContext,
    GlobalContextExploration,
    MypAtlSkill,
    MypInquiryQuestion,
    MypAtlDevelop,
    MypInquiryQuestionIdu,
    MypAtlDevelopIdu
    )

def get_myp_objective_queryset():
    return MypObjective.objects.all().select_related(
        'group',
        )

def get_strand_queryset():
    return Strand.objects.all().select_related(
        'objective',
        )

def get_strand_level_queryset():
    return StrandLevel.objects.all().select_related(
        'strand',
        'achieve_levels',
        )

def get_strand_level_achievement_queryset():
    return StrandLevelAchievement.objects.all().select_related(
        'level',
        )

def get_myp_aim_queryset():
    return MypAim.objects.all().select_related(
        'group',
        )

def get_myp_key_concept_queryset():
    return MypKeyConcept.objects.all().prefetch_related(
        'subjects_recomends',
        )

def get_myp_related_concept_queryset():
    return MypRelatedConcept.objects.all().prefetch_related(
        'disciplines',
    )

def get_global_context_queryset():
    return GlobalContext.objects.all()

def get_global_context_exploration_queryset():
    return GlobalContextExploration.objects.all().select_related(
        'global_context',
    )

def get_myp_atl_skill_queryset():
    return MypAtlSkill.objects.all().select_related(
        'cluster',
    )

def get_myp_unit_planner_queryset():
    return MypUnitPlanner.objects.all().select_related(
        'year'
        'global_context',
        ).prefetch_related(
            'teachers',
            'authors',
            'teacher_roles',
            'ibprofiles',
            'reflection_posts',
            )

def get_myp_inquiry_question_queryset():
    return MypInquiryQuestion.objects.all()

def get_myp_atl_develop_queryset():
    return MypAtlDevelop.objects.all().select_related(
        'atl',
        'strand'
    )

def get_myp_inquiry_question_idu_queryset():
    return MypInquiryQuestionIdu.objects.all()

def get_myp_atl_develop_idu_queryset():
    return MypAtlDevelopIdu.objects.all().select_related(
        'atl',
        'strand'
    )

def get_myp_unit_planner_id_queryset():
    return MypUnitPlannerId.objects.all().select_related(
        'year'
        ).prefetch_related(
            'teachers',
            'authors',
            'reflection_posts',
            )