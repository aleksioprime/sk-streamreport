from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated

from apps.units.myp.serializers import (
    MypUnitPlannerInterdisciplinaryListSerializer,
    MypUnitPlannerInterdisciplinaryRetrieveSerializer,
    MypUnitPlannerInterdisciplinaryCreateSerializer,
    MypUnitPlannerInterdisciplinaryUpdateSerializer,
    MypObjectiveListSerializer,
    StrandListSerializer,
    StrandLevelListSerializer,
    StrandLevelAchievementListSerializer,
    MypAimListSerializer,
    MypKeyConceptListSerializer,
    MypRelatedConceptListSerializer,
    GlobalContextListSerializer,
    GlobalContextExplorationListSerializer,
    MypAtlSkillListSerializer,
    MypUnitPlannerListSerializer,
    MypUnitPlannerRetrieveSerializer,
    MypUnitPlannerCreateSerializer,
    MypUnitPlannerUpdateSerializer,
    MypInquiryQuestionListSerializer,
    MypInquiryQuestionUpdateSerializer,
    MypAtlDevelopListSerializer,
    MypAtlDevelopUpdateSerializer,
    MypInquiryQuestionIduListSerializer,
    MypInquiryQuestionIduUpdateSerializer,
    MypAtlDevelopIduListSerializer,
    MypAtlDevelopIduUpdateSerializer,
)

from apps.units.myp.services import (
    get_myp_unit_planner_queryset,
    get_myp_unit_planner_interdisciplinary_queryset,
    get_myp_objective_queryset,
    get_strand_queryset,
    get_strand_level_queryset,
    get_strand_level_achievement_queryset,
    get_myp_aim_queryset,
    get_myp_key_concept_queryset,
    get_myp_related_concept_queryset,
    get_global_context_queryset,
    get_global_context_exploration_queryset,
    get_myp_atl_skill_queryset,
    get_myp_inquiry_question_queryset,
    get_myp_inquiry_question_idu_queryset,
    get_myp_atl_develop_queryset,
    get_myp_atl_develop_idu_queryset,
)

from apps.units.myp.filters import (
    MypObjectiveFilter,
    StrandFilter,
    StrandLevelFilter,
    StrandLevelAchievementFilter,
    MypAimFilter,
    MypKeyConceptFilter,
    MypRelatedConceptFilter,
    GlobalContextExplorationFilter,
    MypUnitPlannerFilter,
    MypInquiryQuestionFilter,
    MypInquiryQuestionIduFilter,
    MypAtlDevelopFilter,
    MypAtlDevelopIduFilter,
    MypUnitPlannerInterdisciplinaryFilter,
)

# Предметные цели в MYP: список
@extend_schema_view(
    list=extend_schema(summary='Вывод списка предметных целей в MYP', tags=['MYP: Предметные цели']),
    )
class MypObjectiveViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_myp_objective_queryset()
    serializer_class = MypObjectiveListSerializer
    filterset_class = MypObjectiveFilter

# Стрэнды предметных целей в MYP: список
@extend_schema_view(
    list=extend_schema(summary='Вывод списка стрэндов предметных целей в MYP', tags=['MYP: Стрэнды предметных целей']),
    )
class StrandViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_strand_queryset()
    serializer_class = StrandListSerializer
    filterset_class = StrandFilter

# Стрэнды предметных целей по уровням и годам обучения в MYP: список
@extend_schema_view(
    list=extend_schema(summary='Вывод списка стрэндов предметных целей по уровням и годам обучения в MYP', tags=['MYP: Стрэнды по уровням и годам обучения']),
    )
class StrandLevelViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_strand_level_queryset()
    serializer_class = StrandLevelListSerializer
    filterset_class = StrandLevelFilter

# Уровни достижений предметных целей в MYP: список
@extend_schema_view(
    list=extend_schema(summary='Вывод списка уровней достижений предметных целей в MYP', tags=['MYP: Уровни достижений предметных целей']),
    )
class StrandLevelAchievementViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_strand_level_achievement_queryset()
    serializer_class = StrandLevelAchievementListSerializer
    filterset_class = StrandLevelAchievementFilter
    
# Цели предметных групп MYP: список
@extend_schema_view(
    list=extend_schema(summary='Вывод списка целей предметных групп в MYP', tags=['MYP: Цели предметных групп']),
    )
class MypAimViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_myp_aim_queryset()
    serializer_class = MypAimListSerializer
    filterset_class = MypAimFilter

# Ключевые концепты в MYP: список
@extend_schema_view(
    list=extend_schema(summary='Вывод списка ключевых концептов в MYP', tags=['MYP: Ключевые концепты']),
    )
class MypKeyConceptViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_myp_key_concept_queryset()
    serializer_class = MypKeyConceptListSerializer
    filterset_class = MypKeyConceptFilter

# Сопутствующие концепты в MYP: список
@extend_schema_view(
    list=extend_schema(summary='Вывод списка сопутствующих концептов в MYP', tags=['MYP: Сопутствующие концепты']),
    )
class MypRelatedConceptViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_myp_related_concept_queryset()
    serializer_class = MypRelatedConceptListSerializer
    filterset_class = MypRelatedConceptFilter

# Глобальные контексты в MYP: список
@extend_schema_view(
    list=extend_schema(summary='Вывод списка глобальных контекстов в MYP', tags=['MYP: Глобальные контексты']),
    )
class GlobalContextViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_global_context_queryset()
    serializer_class = GlobalContextListSerializer

# Линии исследований в глобальных контекстов в MYP: список
@extend_schema_view(
    list=extend_schema(summary='Вывод списка линий исследований глобальных контекстов в MYP', tags=['MYP: Линии исследований глобальных контекстов']),
    )
class GlobalContextExplorationViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_global_context_exploration_queryset()
    serializer_class = GlobalContextExplorationListSerializer
    filterset_class = GlobalContextExplorationFilter

# Навыки ATL в MYP: список
@extend_schema_view(
    list=extend_schema(summary='Вывод списка навыков ATL в MYP', tags=['MYP: Навыки ATL']),
    )
class MypAtlSkillViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_myp_atl_skill_queryset()
    serializer_class = MypAtlSkillListSerializer

# Юниты MYP: список, просмотр, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка юнитов MYP', tags=['MYP: Юниты']),
    create=extend_schema(summary='Создание юнита MYP', tags=['MYP: Юниты']),
    retrieve=extend_schema(summary='Просмотр юнита MYP', tags=['MYP: Юниты']),
    update=extend_schema(summary='Обновление юнита MYP', tags=['MYP: Юниты']),
    partial_update=extend_schema(summary='Частичное обновление юнита MYP', tags=['MYP: Юниты']),
    destroy=extend_schema(summary='Удаление юнита MYP', tags=['MYP: Юниты']),
    )
class MypUnitPlannerViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    filterset_class = MypUnitPlannerFilter

    def get_queryset(self):
        return get_myp_unit_planner_queryset()
    
    def get_serializer_class(self):
        if self.action == "list":
            return MypUnitPlannerListSerializer
        elif self.action == "retrieve":
            return MypUnitPlannerRetrieveSerializer
        elif self.action == "create":
            return MypUnitPlannerCreateSerializer
        return MypUnitPlannerUpdateSerializer

# Исследовательские вопросы в юните MYP: список, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка исследовательских вопросов в юните MYP', tags=['MYP: Юниты. Исследовательские вопросы']),
    create=extend_schema(summary='Создание исследовательского вопроса в юните MYP', tags=['MYP: Юниты. Исследовательские вопросы']),
    update=extend_schema(summary='Обновление исследовательского вопроса в юните MYP', tags=['MYP: Юниты. Исследовательские вопросы']),
    destroy=extend_schema(summary='Удаление исследовательского вопроса в юните MYP', tags=['MYP: Юниты. Исследовательские вопросы']),
    )
class MypInquiryQuestionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_myp_inquiry_question_queryset()
    filterset_class = MypInquiryQuestionFilter
    
    def get_serializer_class(self):
        if self.action == "list":
            return MypInquiryQuestionListSerializer
        return MypInquiryQuestionUpdateSerializer
    
# Развитие ATL-навыков в юните MYP: список, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка пунктов развития ATL-навыков в юните MYP', tags=['MYP: Юниты. Развитие ATL-навыков']),
    create=extend_schema(summary='Создание пункта развития ATL-навыков в юните MYP', tags=['MYP: Юниты. Развитие ATL-навыков']),
    update=extend_schema(summary='Обновление пункта развития ATL-навыков в юните MYP', tags=['MYP: Юниты. Развитие ATL-навыков']),
    destroy=extend_schema(summary='Удаление пункта развития ATL-навыков в юните MYP', tags=['MYP: Юниты. Развитие ATL-навыков']),
    )
class MypAtlDevelopViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_myp_atl_develop_queryset()
    filterset_class = MypAtlDevelopFilter
    
    def get_serializer_class(self):
        if self.action == "list":
            return MypAtlDevelopListSerializer
        return MypAtlDevelopUpdateSerializer
    
# Исследовательские вопросы в междисциплинарном юните MYP: список, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка исследовательских вопросов в междисциплинарном юните MYP', tags=['MYP: Юниты МД. Исследовательские вопросы']),
    create=extend_schema(summary='Создание исследовательского вопроса в междисциплинарном юните MYP', tags=['MYP: Юниты МД. Исследовательские вопросы']),
    update=extend_schema(summary='Обновление исследовательского вопроса в междисциплинарном юните MYP', tags=['MYP: Юниты МД. Исследовательские вопросы']),
    destroy=extend_schema(summary='Удаление исследовательского вопроса в междисциплинарном юните MYP', tags=['MYP: Юниты МД. Исследовательские вопросы']),
    )
class MypInquiryQuestionIduViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_myp_inquiry_question_idu_queryset()
    filterset_class = MypInquiryQuestionIduFilter
    
    def get_serializer_class(self):
        if self.action == "list":
            return MypInquiryQuestionIduListSerializer
        return MypInquiryQuestionIduUpdateSerializer

# Развитие ATL-навыков в междисциплинарном юните MYP: список, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка пунктов развития ATL-навыков в междисциплинарном юните MYP', tags=['MYP: Юниты МД. Развитие ATL-навыков']),
    create=extend_schema(summary='Создание пункта развития ATL-навыков в междисциплинарном юните MYP', tags=['MYP: Юниты МД. Развитие ATL-навыков']),
    update=extend_schema(summary='Обновление пункта развития ATL-навыков в междисциплинарном юните MYP', tags=['MYP: Юниты МД. Развитие ATL-навыков']),
    destroy=extend_schema(summary='Удаление пункта развития ATL-навыков в междисциплинарном юните MYP', tags=['MYP: Юниты МД. Развитие ATL-навыков']),
    )
class MypAtlDevelopIduViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_myp_atl_develop_idu_queryset()
    filterset_class = MypAtlDevelopIduFilter
    
    def get_serializer_class(self):
        if self.action == "list":
            return MypAtlDevelopIduListSerializer
        return MypAtlDevelopIduUpdateSerializer

# Междисциплинарные юниты MYP: список, просмотр, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка междисцплинарных юнитов MYP', tags=['MYP: Юниты МД']),
    create=extend_schema(summary='Создание междисцплинарного юнита MYP', tags=['MYP: Юниты МД']),
    retrieve=extend_schema(summary='Просмотр междисцплинарного юнита MYP', tags=['MYP: Юниты МД']),
    update=extend_schema(summary='Обновление междисцплинарного юнита MYP', tags=['MYP: Юниты МД']),
    partial_update=extend_schema(summary='Частичное обновление междисцплинарного юнита MYP', tags=['MYP: Юниты МД']),
    destroy=extend_schema(summary='Удаление междисцплинарного юнита MYP', tags=['MYP: Юниты МД']),
    )
class MypUnitPlannerInterdisciplinaryViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    filterset_class = MypUnitPlannerInterdisciplinaryFilter

    def get_queryset(self):
        return get_myp_unit_planner_interdisciplinary_queryset()

    def get_serializer_class(self):
        if self.action == "list":
            return MypUnitPlannerInterdisciplinaryListSerializer
        elif self.action == "retrieve":
            return MypUnitPlannerInterdisciplinaryRetrieveSerializer
        elif self.action == "create":
            return MypUnitPlannerInterdisciplinaryCreateSerializer
        return MypUnitPlannerInterdisciplinaryUpdateSerializer
    
    