import django_filters

from apps.units.pyp.models import (
    PypUnitPlanner,
    PypLinesOfInquiry,
    PypRelatedConcept,
    PypAtlDevelop,
    PypAtlSkill,
    PypAtlCluster
)

class PypUnitPlannerFilter(django_filters.FilterSet):
    class Meta:
        model = PypUnitPlanner
        fields = {'authors', 'teachers', 'year'}

class PypLinesOfInquiryFilter(django_filters.FilterSet):
    class Meta:
        model = PypLinesOfInquiry
        fields = {'unit'}

class PypRelatedConceptFilter(django_filters.FilterSet):
    class Meta:
        model = PypRelatedConcept
        fields = {'unit'}

class PypAtlDevelopFilter(django_filters.FilterSet):
    class Meta:
        model = PypAtlDevelop
        fields = {'unit'}

class PypAtlSkillFilter(django_filters.FilterSet):
    class Meta:
        model = PypAtlSkill
        fields = {'cluster'}

class PypAtlClusterFilter(django_filters.FilterSet):
    class Meta:
        model = PypAtlCluster
        fields = {'category'}