import django_filters

from apps.units.dp.models import (
    DpUnitPlanner,
    DpAim,
    DpObjective,
    CourseContent,
    Criterion,
    DpInquiryQuestion,
    DpAtlDevelop
)

class DpUnitPlannerFilter(django_filters.FilterSet):
    class Meta:
        model = DpUnitPlanner
        fields = {'authors', 'teachers', 'year'}

class DpAimFilter(django_filters.FilterSet):
    class Meta:
        model = DpAim
        fields = {'discipline'}

class DpObjectiveFilter(django_filters.FilterSet):
    class Meta:
        model = DpObjective
        fields = {'discipline'}

class CourseContentFilter(django_filters.FilterSet):
    class Meta:
        model = CourseContent
        fields = {'topic__discipline'}

class CriterionFilter(django_filters.FilterSet):
    class Meta:
        model = Criterion
        fields = {'discipline'}

class DpInquiryQuestionFilter(django_filters.FilterSet):
    class Meta:
        model = DpInquiryQuestion
        fields = {'unit'}

class DpAtlDevelopFilter(django_filters.FilterSet):
    class Meta:
        model = DpAtlDevelop
        fields = {'unit'}