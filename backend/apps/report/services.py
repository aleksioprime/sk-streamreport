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
    ReportIbProfile,
    ReportMentor,
    ReportPrimaryUnit,
    ReportMentorPrimary,
    ReportExtra,
)

def get_report_period_queryset():
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

def get_report_ibprofile_queryset():
    return ReportIbProfile.objects.all().select_related(
        'profile',
        )

def get_report_mentor_queryset():
    return ReportMentor.objects.all().select_related(
        'student',
        'author',
        'period',
        'group',
        ).prefetch_related(
            'profiles',
            )

def get_report_primary_unit_queryset():
    return ReportPrimaryUnit.objects.all().select_related(
        'unit',
        )

def get_report_mentor_primary_queryset():
    return ReportMentorPrimary.objects.all().select_related(
        'student',
        'author',
        'period',
        'group',
        ).prefetch_related(
            'profiles',
            'pyp_units',
            )

def get_report_extra_queryset():
    return ReportExtra.objects.all().select_related(
        'student',
        'author',
        'period',
        'group',
        )