import django_filters
from django.db.models import Q

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
    ReportIbProfile,
    ReportMentor,
    ReportPrimaryUnit,
    ReportMentorPrimary,
    ReportExtra
)

from general.models import (
    User
)

class ReportPeriodFilter(django_filters.FilterSet):
    class Meta:
        model = ReportPeriod
        fields = {'year'}

class ReportCriterionFilter(django_filters.FilterSet):
    class Meta:
        model = ReportCriterion
        fields = {'subjects', 'years'}
    def filter_queryset(self, queryset):
        subjects = self.request.query_params.get('subjects', None)
        years = self.request.query_params.get('years', None)
        # queryset = super(ReportCriterionFilter, self).filter_queryset(queryset)
        if years is not None:
            queryset = queryset.filter(years=years)
        if subjects is not None:
            queryset = queryset.filter(Q(subjects=subjects) | Q(subjects__isnull=True))
        else:
            queryset = queryset.filter(subjects__isnull=True)
        return queryset

# class ReportCriterionLevelFilter(django_filters.FilterSet):
#     class Meta:
#         model = ReportCriterionLevel
#         fields = {'criterions'}

class ReportCriterionAchievementFilter(django_filters.FilterSet):
    class Meta:
        model = ReportCriterionAchievement
        fields = {'report', 'report_extra', 'report_mentor'}

class ReportPrimaryTopicFilter(django_filters.FilterSet):
    class Meta:
        model = ReportPrimaryTopic
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

class ReportIbProfileFilter(django_filters.FilterSet):
    class Meta:
        model =  ReportIbProfile
        fields = {'report'}

class ReportMentorFilter(django_filters.FilterSet):
    class Meta:
        model = ReportMentor
        fields = {'student', 'author', 'period', 'group'}

class ReportPrimaryUnitFilter(django_filters.FilterSet):
    class Meta:
        model =  ReportPrimaryUnit
        fields = {'report'}

class ReportMentorPrimaryFilter(django_filters.FilterSet):
    class Meta:
        model = ReportMentorPrimary
        fields = {'student', 'author', 'period', 'group'}

class ReportExtraFilter(django_filters.FilterSet):
    class Meta:
        model = ReportExtra
        fields = {'student', 'author', 'period', 'group'}

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = {'groups', 'classes'}