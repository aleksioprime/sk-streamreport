from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated

from apps.units.dp.serializers import (
    DpUnitPlannerListSerializer,
    DpUnitPlannerRetrieveSerializer,
    DpUnitPlannerCreateSerializer,
    DpUnitPlannerUpdateSerializer,
    DpAimListSerializer,
    DpObjectiveListSerializer,
    CourseContentListSerializer,
    CriterionListSerializer,
    DpAtlSkillListSerializer,
    DpInquiryQuestionListSerializer,
    DpInquiryQuestionUpdateSerializer,
    DpAtlDevelopListSerializer,
    DpAtlDevelopUpdateSerializer
)

from apps.units.dp.services import (
    get_dp_unit_planner_queryset,
    get_dp_aim_queryset,
    get_dp_objective_queryset,
    get_course_content_queryset,
    get_criterion_queryset,
    get_dp_atl_skill_queryset,
    get_dp_inquiry_question_queryset,
    get_dp_atl_develop_queryset
)

from apps.units.dp.filters import (
    DpUnitPlannerFilter,
    DpAimFilter,
    DpObjectiveFilter,
    CourseContentFilter,
    CriterionFilter,
    DpInquiryQuestionFilter,
    DpAtlDevelopFilter
)

# Юниты DP: список, просмотр, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка юнитов DP', tags=['DP: Юниты']),
    create=extend_schema(summary='Создание юнита DP', tags=['DP: Юниты']),
    retrieve=extend_schema(summary='Просмотр юнита DP', tags=['DP: Юниты']),
    update=extend_schema(summary='Обновление юнита DP', tags=['DP: Юниты']),
    partial_update=extend_schema(summary='Частичное обновление юнита DP', tags=['DP: Юниты']),
    destroy=extend_schema(summary='Удаление юнита DP', tags=['DP: Юниты']),
    )
class DpUnitPlannerViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    filterset_class = DpUnitPlannerFilter
    def get_queryset(self):
        return get_dp_unit_planner_queryset()

    def get_serializer_class(self):
        if self.action == "list":
            return DpUnitPlannerListSerializer
        elif self.action == "retrieve":
            return DpUnitPlannerRetrieveSerializer
        elif self.action == "create":
            return DpUnitPlannerCreateSerializer
        return DpUnitPlannerUpdateSerializer
    
# Цели предметных групп DP: список
@extend_schema_view(
    list=extend_schema(summary='Вывод списка целей предметных групп в DP', tags=['DP: Цели предметных групп']),
    )
class DpAimViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_dp_aim_queryset()
    serializer_class = DpAimListSerializer
    filterset_class = DpAimFilter

# Предметные цели в DP: список
@extend_schema_view(
    list=extend_schema(summary='Вывод списка предметных целей в DP', tags=['DP: Предметные цели']),
    )
class DpObjectiveViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_dp_objective_queryset()
    serializer_class = DpObjectiveListSerializer
    filterset_class = DpObjectiveFilter

# Учебные темы курсов в DP: список
@extend_schema_view(
    list=extend_schema(summary='Вывод списка учебных тем курсов в DP', tags=['DP: Учебные темы курсов']),
    )
class CourseContentViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_course_content_queryset()
    serializer_class = CourseContentListSerializer
    filterset_class = CourseContentFilter

# Критерии оценивания в DP: список
@extend_schema_view(
    list=extend_schema(summary='Вывод списка критерив оценивания в DP', tags=['DP: Критерии оценивания']),
    )
class CriterionViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_criterion_queryset()
    serializer_class = CriterionListSerializer
    filterset_class = CriterionFilter

# Навыки ATL в DP: список
@extend_schema_view(
    list=extend_schema(summary='Вывод списка навыков ATL в DP', tags=['DP: Навыки ATL']),
    )
class DpAtlSkillViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_dp_atl_skill_queryset()
    serializer_class = DpAtlSkillListSerializer

# Исследовательские вопросы в юните DP: список, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка исследовательских вопросов в юните DP', tags=['DP: Юниты. Исследовательские вопросы']),
    create=extend_schema(summary='Создание исследовательского вопроса в юните DP', tags=['DP: Юниты. Исследовательские вопросы']),
    update=extend_schema(summary='Обновление исследовательского вопроса в юните DP', tags=['DP: Юниты. Исследовательские вопросы']),
    destroy=extend_schema(summary='Удаление исследовательского вопроса в юните DP', tags=['DP: Юниты. Исследовательские вопросы']),
    )
class DpInquiryQuestionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_dp_inquiry_question_queryset()
    filterset_class = DpInquiryQuestionFilter
    
    def get_serializer_class(self):
        if self.action == "list":
            return DpInquiryQuestionListSerializer
        return DpInquiryQuestionUpdateSerializer
    
# Развитие ATL-навыков в юните DP: список, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка пунктов развития ATL-навыков в юните DP', tags=['DP: Юниты. Развитие ATL-навыков']),
    create=extend_schema(summary='Создание пункта развития ATL-навыков в юните DP', tags=['DP: Юниты. Развитие ATL-навыков']),
    update=extend_schema(summary='Обновление пункта развития ATL-навыков в юните DP', tags=['DP: Юниты. Развитие ATL-навыков']),
    destroy=extend_schema(summary='Удаление пункта развития ATL-навыков в юните DP', tags=['DP: Юниты. Развитие ATL-навыков']),
    )
class DpAtlDevelopViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_dp_atl_develop_queryset()
    filterset_class = DpAtlDevelopFilter
    
    def get_serializer_class(self):
        if self.action == "list":
            return DpAtlDevelopListSerializer
        return DpAtlDevelopUpdateSerializer