from django.urls import path
from curriculum.views import UnitPlannerMYPViewEdit, UnitPlannerMYPListCreate, TeacherViewSet, ClassYearViewSet, \
    SubjectViewSet, CriterionViewSet, DepartmentViewSet, LearnerProfileIBViewSet, SkillATLViewSet, ObjectiveViewSet, StrandViewSet, \
    AimViewSet, GlobalContextViewSet, ExplorationToDevelopViewSet, KeyConceptViewSet, RelatedConceptViewSet, \
    InQuestionMYPViewSet, ATLMappingMYPViewSet, ReflectionMYPViewSet, LevelViewSet, UnitPlannerMYPIDViewSet, \
    UnitExport

urlpatterns = [
    path('myp/unit', UnitPlannerMYPListCreate.as_view({'get': 'list', 'post': 'create'})),
    path('myp/unit/<int:pk>', UnitPlannerMYPViewEdit.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('departments', DepartmentViewSet.as_view({'get': 'list'})),
    path('teachers', TeacherViewSet.as_view({'get': 'list'})),
    path('myp/years', ClassYearViewSet.as_view({'get': 'list'})),
    path('myp/levels', LevelViewSet.as_view({'get': 'list'})),
    path('myp/subjects', SubjectViewSet.as_view({'get': 'list'})),
    path('myp/criteria', CriterionViewSet.as_view({'get': 'list'})),
    path('ibprofile', LearnerProfileIBViewSet.as_view({'get': 'list'})),
    path('atlskills', SkillATLViewSet.as_view({'get': 'list'})),
    path('objectives', ObjectiveViewSet.as_view({'get': 'list'})),
    path('myp/strands', StrandViewSet.as_view({'get': 'list'})),
    path('aims', AimViewSet.as_view({'get': 'list'})),
    path('myp/gcontext', GlobalContextViewSet.as_view({'get': 'list'})),
    path('explorations', ExplorationToDevelopViewSet.as_view({'get': 'list'})),
    path('myp/kconcepts', KeyConceptViewSet.as_view({'get': 'list'})),
    path('rconcepts', RelatedConceptViewSet.as_view({'get': 'list'})),
    path('unitplans/myp/export', UnitExport.as_view()),
    path('unitplans/myp/inquestion', InQuestionMYPViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('unitplans/myp/inquestion/<int:pk>', InQuestionMYPViewSet.as_view({'put': 'update', 'delete': 'destroy' })),
    path('unitplans/myp/atlmapping', ATLMappingMYPViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('unitplans/myp/atlmapping/<int:pk>', ATLMappingMYPViewSet.as_view({'put': 'update', 'delete': 'destroy' })),
    path('unitplans/myp/reflection', ReflectionMYPViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('unitplans/myp/reflection/<int:pk>', ReflectionMYPViewSet.as_view({'put': 'update', 'delete': 'destroy' })),
    path('unitplans/myp/inter', UnitPlannerMYPIDViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('unitplans/myp/inter/<int:pk>', UnitPlannerMYPIDViewSet.as_view({'put': 'update', 'delete': 'destroy' })),
    # path('unitplans/myp/subject', SubjectLevelMYPViewSet.as_view({'get': 'list', 'post': 'create'})),
    # path('unitplans/myp/subject/<int:pk>', SubjectLevelMYPViewSet.as_view({'put': 'update', 'delete': 'destroy' })),
]