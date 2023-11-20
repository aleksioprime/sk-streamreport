import django_filters

from apps.report.models import (
    ReportTeacherPrimary,
)

class ReportTeacherPrimaryFilter(django_filters.FilterSet):
    class Meta:
        model = ReportTeacherPrimary
        fields = {'student', 'author', 'subject', 'period', 'group'}