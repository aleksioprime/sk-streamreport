import django_filters

from apps.units.myp.models import (
    StrandLevelAchievement,
    StrandLevel,
    Strand,
    MypObjective,
    MypAim,
    MypKeyConcept,
    MypRelatedConcept,
    GlobalContextExploration,
    MypUnitPlanner,
    MypInquiryQuestion,
    MypAtlDevelop,
    MypInquiryQuestionIdu,
    MypAtlDevelopIdu,
    MypUnitPlannerInterdisciplinary
)

class MypObjectiveFilter(django_filters.FilterSet):
    class Meta:
        model = MypObjective
        fields = {'group'}

class StrandFilter(django_filters.FilterSet):
    class Meta:
        model = Strand
        fields = {'objective'}

class StrandLevelFilter(django_filters.FilterSet):
    class Meta:
        model = StrandLevel
        fields = {'strand'}

class StrandLevelAchievementFilter(django_filters.FilterSet):
    class Meta:
        model = StrandLevelAchievement
        fields = {'level'}

class MypAimFilter(django_filters.FilterSet):
    class Meta:
        model = MypAim
        fields = {'group'}

class MypKeyConceptFilter(django_filters.FilterSet):
    class Meta:
        model = MypKeyConcept
        fields = {'groups'}

class MypRelatedConceptFilter(django_filters.FilterSet):
    class Meta:
        model = MypRelatedConcept
        fields = {'disciplines'}

class GlobalContextExplorationFilter(django_filters.FilterSet):
    class Meta:
        model = GlobalContextExploration
        fields = {'global_context'}

class MypUnitPlannerFilter(django_filters.FilterSet):
    class Meta:
        model = MypUnitPlanner
        fields = {'authors', 'teachers', 'year', 'global_context'}

class MypInquiryQuestionFilter(django_filters.FilterSet):
    class Meta:
        model = MypInquiryQuestion
        fields = {'unit'}

class MypAtlDevelopFilter(django_filters.FilterSet):
    class Meta:
        model = MypAtlDevelop
        fields = {'unit'}

class MypInquiryQuestionIduFilter(django_filters.FilterSet):
    class Meta:
        model = MypInquiryQuestionIdu
        fields = {'unit'}

class MypAtlDevelopIduFilter(django_filters.FilterSet):
    class Meta:
        model = MypAtlDevelopIdu
        fields = {'unit'}

class MypUnitPlannerInterdisciplinaryFilter(django_filters.FilterSet):
    class Meta:
        model = MypUnitPlannerInterdisciplinary
        fields = {'authors', 'teachers', 'year'}