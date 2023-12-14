from apps.units.dp.models import (
    DpUnitPlanner,
    DpObjective,
    DpAim,
    CourseContent,
    Criterion,
    DpAtlSkill,
    DpInquiryQuestion,
    DpAtlDevelop
    )

def get_dp_unit_planner_queryset():
    return DpUnitPlanner.objects.all().order_by("title")

def get_dp_aim_queryset():
    return DpAim.objects.all().select_related(
        'discipline__group',
        )

def get_dp_objective_queryset():
    return DpObjective.objects.all().select_related(
        'discipline__group',
        ).prefetch_related(
        'items',
        )

def get_course_content_queryset():
    return CourseContent.objects.all().select_related(
        'topic',
        'topic__discipline',
        'topic__discipline__group',
        )

def get_criterion_queryset():
    return Criterion.objects.all().select_related(
        'discipline',
        'discipline__group',
        )

def get_dp_atl_skill_queryset():
    return DpAtlSkill.objects.all().select_related(
        'cluster',
        'cluster__category',
        )

def get_dp_inquiry_question_queryset():
    return DpInquiryQuestion.objects.all()

def get_dp_atl_develop_queryset():
    return DpAtlDevelop.objects.all().select_related(
        'atl',
    )