import django_filters

from apps.report.models import (
    ReportPeriod,
    ReportCriterion,
    ReportCriterionLevel,
    ReportCriterionAchievement,
    ReportTeacherPrimary,
    ReportPrimaryTopic,
    ReportSecondaryCriterion,
    ReportSecondaryLevel,
    ReportTeacherSecondary,
    ReportTeacherHigh,
)

class ReportPeriodFilter(django_filters.FilterSet):
    class Meta:
        model = ReportPeriod
        fields = {'year'}

class ReportCriterionFilter(django_filters.FilterSet):
    class Meta:
        model = ReportCriterion
        fields = {'subjects', 'author', 'years'}

class ReportCriterionLevelFilter(django_filters.FilterSet):
    class Meta:
        model = ReportCriterionLevel
        fields = {'criterion'}

class ReportCriterionAchievementFilter(django_filters.FilterSet):
    class Meta:
        model = ReportCriterionAchievement
        fields = {'report'}

class ReportPrimaryTopicFilter(django_filters.FilterSet):
    class Meta:
        model =  ReportPrimaryTopic
        fields = {'report'}

class ReportTeacherPrimaryFilter(django_filters.FilterSet):
    class Meta:
        model = ReportTeacherPrimary
        fields = {'student', 'author', 'subject', 'period', 'group'}

class ReportSecondaryCriterionFilter(django_filters.FilterSet):
    class Meta:
        model =  ReportSecondaryCriterion
        fields = {'report'}
        
class ReportSecondaryLevelFilter(django_filters.FilterSet):
    class Meta:
        model =  ReportSecondaryLevel
        fields = {'report'}

class ReportTeacherSecondaryFilter(django_filters.FilterSet):
    class Meta:
        model = ReportTeacherSecondary
        fields = {'student', 'author', 'subject', 'period', 'group'}

class ReportTeacherHighFilter(django_filters.FilterSet):
    class Meta:
        model = ReportTeacherHigh
        fields = {'student', 'author', 'subject', 'period', 'group'}