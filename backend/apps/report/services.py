from apps.report.models import (
    ReportPeriod,
    ReportCriterion,
    ReportCriterionLevel,
    ReportCriterionAchievement,
    ReportPrimaryTopic,
    ReportTeacherPrimary,
    ReportSecondaryCriterion,
    ReportSecondaryLevel,
    ReportTeacherSecondary,
    ReportTeacherHigh,
)

def get_report_report_queryset():
    return ReportPeriod.objects.all().select_related(
        'year',
        )

def get_report_criterion_queryset():
    return ReportCriterion.objects.all().select_related(
        'author',
        ).prefetch_related(
            'subjects',
            'years'
            )

def get_report_criterion_level_queryset():
    return ReportCriterionLevel.objects.all()

def get_report_criterion_achievement_queryset():
    return ReportCriterionAchievement.objects.all().select_related(
        'criterion',
        'achievement'
        )

def get_report_primary_achievement_queryset():
    return ReportPrimaryTopic.objects.all().select_related(
        'topic',
        )

def get_report_teacher_primary_queryset():
    return ReportTeacherPrimary.objects.all().select_related(
        'student',
        'author',
        'period',
        'group',
        'subject'
        ).prefetch_related(
            'criterion_achievements',
            'topic_achievements'
            )

def get_report_secondary_criterion_queryset():
    return ReportSecondaryCriterion.objects.all().select_related(
        'criterion',
        )

def get_report_secondary_level_queryset():
    return ReportSecondaryLevel.objects.all().select_related(
        'objective',
        'level',
        )

def get_report_teacher_secondary_queryset():
    return ReportTeacherSecondary.objects.all().select_related(
        'student',
        'author',
        'period',
        'group',
        'subject'
        ).prefetch_related(
            'criterion_achievements',
            'criterion_marks',
            'objective_levels'
            )

def get_report_teacher_high_queryset():
    return ReportTeacherHigh.objects.all().select_related(
        'student',
        'author',
        'period',
        'group',
        'subject'
        ).prefetch_related(
            'criterion_achievements',
            )