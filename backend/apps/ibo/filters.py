import django_filters

from apps.ibo.models import (
    IbProfileDevelop,
    UnitReflectionPost
)

class IbProfileDevelopFilter(django_filters.FilterSet):
    class Meta:
        model = IbProfileDevelop
        fields = {'unit'}

class UnitReflectionPostFilter(django_filters.FilterSet):
    class Meta:
        model = UnitReflectionPost
        fields = {'unit', 'author'}