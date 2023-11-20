from apps.report.models import (
    ReportTeacherPrimary,
)

def get_peport_teacher_primary_queryset():
    return ReportTeacherPrimary.objects.all().select_related(
        'student',
        'author',
        'period',
        'group',
        'subject'
        ).prefetch_related(
            'units',
            'report_units',
            'profiles',
            'achievements'
            )