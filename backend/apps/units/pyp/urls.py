from django.urls import path

from apps.units.pyp.views import (
    PypUnitPlannerViewSet,
    TransdisciplinaryThemeViewSet,
    PypKeyConceptViewSet,
    PypAtlSkillViewSet,
    PypLinesOfInquiryViewSet,
    PypRelatedConceptViewSet,
    PypAtlDevelopViewSet,
    PypAtlClusterViewSet,
    )

urlpatterns = [
    path('pyp/transdisciplinary', TransdisciplinaryThemeViewSet.as_view({'get': 'list'})),
    path('pyp/keyconcept', PypKeyConceptViewSet.as_view({'get': 'list'})),
    path('pyp/atl/cluster', PypAtlClusterViewSet.as_view({'get': 'list'})),
    path('pyp/atl/skill', PypAtlSkillViewSet.as_view({'get': 'list'})),
    path('pyp/unit', PypUnitPlannerViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('pyp/unit/<int:pk>', PypUnitPlannerViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('pyp/unit/inquiry', PypLinesOfInquiryViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('pyp/unit/inquiry/<int:pk>', PypLinesOfInquiryViewSet.as_view({'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('pyp/unit/relatedconcept', PypRelatedConceptViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('pyp/unit/relatedconcept/<int:pk>', PypRelatedConceptViewSet.as_view({'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('pyp/unit/atl', PypAtlDevelopViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('pyp/unit/atl/<int:pk>', PypAtlDevelopViewSet.as_view({'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
]