from django.db.models import Prefetch

from apps.report.models import (
    ReportPeriod,
    ReportCriterion,
    ReportCriterionLevel,
    ReportCriterionAchievement,
    ReportPrimaryTopic,
    ReportTeacher,
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

from general.models import (
    User
)

from apps.portfolio.models import (
    EventParticipation,
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
            'years',
            'levels'
            )

def get_report_criterion_level_queryset():
    return ReportCriterionLevel.objects.all()

def get_report_criterion_achievement_queryset():
    return ReportCriterionAchievement.objects.all().select_related(
        'criterion',
        'achievement',
        )

def get_report_primary_achievement_queryset():
    return ReportPrimaryTopic.objects.all().select_related(
        'topic',
        )

def get_report_teacher_primary_queryset(group):
    return ReportTeacherPrimary.objects.all().select_related(
        'student',
        'author',
        'period',
        'period__year',
        'group',
        'group__year_academic',
        'group__year_study',
        'subject',
        ).prefetch_related(
            'criterion_achievements',
            'criterion_achievements__achievement',
            'criterion_achievements__criterion',
            'criterion_achievements__criterion__author',
            'criterion_achievements__criterion__subjects',
            'criterion_achievements__criterion__years',
            'criterion_achievements__criterion__levels',
            'topic_achievements',
            'topic_achievements__topic',
            Prefetch(
                    'student__student_events', 
                    queryset=EventParticipation.objects.filter(group=group)
                ),
            )



def get_report_secondary_criterion_queryset():
    return ReportSecondaryCriterion.objects.all().select_related(
        'criterion',
        )

def get_report_secondary_level_queryset():
    return ReportSecondaryLevel.objects.all().select_related(
        'strand',
        'level',
        ).prefetch_related(
            'strand',
            'strand__achieve_levels',
        )

def get_report_teacher_secondary_queryset(group, student):
    print(f'Параметры запроса: {group}, {student}')
    return ReportTeacherSecondary.objects.select_related(
        'student',
        'author',
        'period',
        'period__year',
        'group',
        'group__year_academic',
        'group__year_study',
        'subject',
        ).prefetch_related(
            'criterion_achievements',
            'criterion_achievements__achievement',
            'criterion_achievements__criterion',
            'criterion_achievements__criterion__author',
            'criterion_achievements__criterion__subjects',
            'criterion_achievements__criterion__years',
            'criterion_achievements__criterion__levels',
            'criterion_marks',
            'criterion_marks__criterion',
            'objective_levels',
            'objective_levels__strand',
            'objective_levels__strand__strand',
            'objective_levels__strand__strand__objective',
            'objective_levels__strand__achieve_levels',
            'objective_levels__level',
            Prefetch(
                    'student__student_events', 
                    queryset=EventParticipation.objects.filter(group=group)
                ),
            )

def get_report_teacher_high_queryset(group):
    return ReportTeacherHigh.objects.all().select_related(
        'student',
        'author',
        'period',
        'period__year',
        'group',
        'group__year_academic',
        'group__year_study',
        'subject',
        ).prefetch_related(
            'criterion_achievements',
            'criterion_achievements__criterion',
            Prefetch(
                    'student__student_events', 
                    queryset=EventParticipation.objects.filter(group=group)
                ),
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

# Запрос на репорты сорудников класса
def get_user_report_extra_queryset(group=None, period=None):
    return User.objects.all().prefetch_related(
        Prefetch(
                'reportextra_student_reports', 
                queryset=ReportExtra.objects.filter(group=group, period=period).select_related(
                    'student',
                    'author',
                    'group',
                    'group__year_academic',
                    'group__year_study',
                ).prefetch_related(
                    'student__student_events',
                    'criterion_achievements',
                    'criterion_achievements__achievement',
                    'criterion_achievements__criterion',
                ), 
            ),
        )

def get_user_report_mentor_primary_queryset(group=None, period=None):
    return User.objects.all().prefetch_related(
        'reportmentor_student_reports',
        Prefetch(
                'reportmentor_student_reports', 
                queryset=ReportMentorPrimary.objects.filter(group=group, period=period), 
                to_attr='filtered_reports'
            ),
        'classes',
        )

def get_user_report_mentor_queryset(group=None, period=None):
    return User.objects.prefetch_related(
        Prefetch(
                'reportmentor_student_reports', 
                queryset=ReportMentor.objects.filter(group=group, period=period).select_related(
                    'author', 
                    'student',
                    'group',
                    'group__year_academic',
                    'group__year_study',
                    ).prefetch_related(
                        'student__student_events',
                        'profiles',
                        'profiles__profile',
                    ), 
            ),
        Prefetch(
                'reportteacher_student_reports', 
                queryset=ReportTeacherPrimary.objects.filter(group=group, period=period).select_related(
                    'author',
                    'subject',
                    ).prefetch_related(
                        'criterion_achievements',
                        'criterion_achievements__achievement',
                        'criterion_achievements__criterion',
                        'topic_achievements',
                        'topic_achievements__topic',
                        ), 
                to_attr='filtered_teacher_primary_reports',
            ),
        Prefetch(
                'reportteacher_student_reports', 
                queryset=ReportTeacherSecondary.objects.filter(group=group, period=period).select_related(
                    'author',
                    'subject',
                    ).prefetch_related(
                        'criterion_achievements',
                        'criterion_achievements__achievement',
                        'criterion_achievements__criterion',
                        'criterion_marks',
                        'criterion_marks__criterion',
                        'objective_levels',
                        'objective_levels__strand',
                        'objective_levels__level',
                    ),  
                to_attr='filtered_teacher_secondary_reports'
            ),
        Prefetch(
                'reportteacher_student_reports', 
                queryset=ReportTeacherHigh.objects.filter(group=group, period=period).select_related(
                    'author',
                    'subject',
                    ).prefetch_related(
                        'criterion_achievements',
                        'criterion_achievements__criterion',
                        'criterion_achievements__achievement',
                        ), 
                to_attr='filtered_teacher_high_reports'
            ),
        Prefetch(
                'reportextra_student_reports', 
                queryset=ReportExtra.objects.filter(group=group, period=period).select_related(
                    'author',
                )
            ),
        )