from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated

from apps.units.pyp.serializers import (
    PypUnitPlannerListSerializer, 
    PypUnitPlannerRetrieveSerializer,
    PypUnitPlannerCreateSerializer,
    PypUnitPlannerUpdateSerializer,
    TransdisciplinaryThemeListSerializer,
    PypKeyConceptListSerializer,
    PypAtlSkillListSerializer,
    PypLinesOfInquiryListSerializer,
    PypLinesOfInquiryUpdateSerializer,
    PypRelatedConceptListSerializer,
    PypRelatedConceptUpdateSerializer,
    PypAtlDevelopListSerializer,
    PypAtlDevelopUpdateSerializer
)

from apps.units.pyp.filters import (
    PypUnitPlannerFilter,
    PypLinesOfInquiryFilter,
    PypRelatedConceptFilter,
    PypAtlDevelopFilter
)

from apps.units.pyp.services import (
    get_pyp_unit_planner_queryset,
    get_transdisciplinary_theme_queryset,
    get_pyp_key_concept_queryset,
    get_pyp_atl_skill_queryset,
    get_pyp_lines_inquiry_queryset,
    get_pyp_related_concept_queryset,
    get_pyp_atl_develop_queryset
)

# Юниты в PYP: список, просмотр, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка юнитов PYP', tags=['PYP: Юниты']),
    create=extend_schema(summary='Создание юнита PYP', tags=['PYP: Юниты']),
    retrieve=extend_schema(summary='Просмотр юнита PYP', tags=['PYP: Юниты']),
    update=extend_schema(summary='Обновление юнита PYP', tags=['PYP: Юниты']),
    partial_update=extend_schema(summary='Частичное обновление юнита PYP', tags=['PYP: Юниты']),
    destroy=extend_schema(summary='Удаление юнита PYP', tags=['PYP: Юниты']),
    )
class PypUnitPlannerViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_pyp_unit_planner_queryset()
    filterset_class = PypUnitPlannerFilter
    
    def get_serializer_class(self):
        if self.action == "list":
            return PypUnitPlannerListSerializer
        elif self.action == "retrieve":
            return PypUnitPlannerRetrieveSerializer
        elif self.action == "create":
            return PypUnitPlannerCreateSerializer
        return PypUnitPlannerUpdateSerializer
    
# Трансдисциплинарные темы в PYP: список
@extend_schema_view(
    list=extend_schema(summary='Вывод списка трансдициплинарных тем в PYP', tags=['PYP: Трансдициплинарные темы']),
    )
class TransdisciplinaryThemeViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_transdisciplinary_theme_queryset()
    serializer_class = TransdisciplinaryThemeListSerializer

# Ключевые концепты в PYP: список
@extend_schema_view(
    list=extend_schema(summary='Вывод списка ключевых концептов в PYP', tags=['PYP: Ключевые концепты']),
    )
class PypKeyConceptViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_pyp_key_concept_queryset()
    serializer_class = PypKeyConceptListSerializer

# Навыки ATL в PYP: список
@extend_schema_view(
    list=extend_schema(summary='Вывод списка навыков ATL в PYP', tags=['PYP: Навыки ATL']),
    )
class PypAtlSkillViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_pyp_atl_skill_queryset()
    serializer_class = PypAtlSkillListSerializer

# Линии исследования в юните PYP: список, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка линий исследования в юните PYP', tags=['PYP: Юниты. Линии исследования']),
    create=extend_schema(summary='Создание линии исследования в юните PYP', tags=['PYP: Юниты. Линии исследования']),
    update=extend_schema(summary='Обновление линии исследования в юните PYP', tags=['PYP: Юниты. Линии исследования']),
    destroy=extend_schema(summary='Удаление линии исследования в юните PYP', tags=['PYP: Юниты. Линии исследования']),
    )
class PypLinesOfInquiryViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_pyp_lines_inquiry_queryset()
    filterset_class = PypLinesOfInquiryFilter
    
    def get_serializer_class(self):
        if self.action == "list":
            return PypLinesOfInquiryListSerializer
        return PypLinesOfInquiryUpdateSerializer
    
# Сопутствующие понятия в юните PYP: список, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка сопутствующих понятий в юните PYP', tags=['PYP: Юниты. Сопутствующие понятия']),
    create=extend_schema(summary='Создание сопутствующего понятия в юните PYP', tags=['PYP: Юниты. Сопутствующие понятия']),
    update=extend_schema(summary='Обновление сопутствующего понятия в юните PYP', tags=['PYP: Юниты. Сопутствующие понятия']),
    destroy=extend_schema(summary='Удаление сопутствующего понятия в юните PYP', tags=['PYP: Юниты. Сопутствующие понятия']),
    )
class PypRelatedConceptViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_pyp_related_concept_queryset()
    filterset_class = PypRelatedConceptFilter
    
    def get_serializer_class(self):
        if self.action == "list":
            return PypRelatedConceptListSerializer
        return PypRelatedConceptUpdateSerializer
    
# Развитие ATL-навыков в юните PYP: список, создание, редактирование и удаление
@extend_schema_view(
    list=extend_schema(summary='Вывод списка пунктов развития ATL-навыков в юните PYP', tags=['PYP: Юниты. Развитие ATL-навыков']),
    create=extend_schema(summary='Создание пункта развития ATL-навыков в юните PYP', tags=['PYP: Юниты. Развитие ATL-навыков']),
    update=extend_schema(summary='Обновление пункта развития ATL-навыков в юните PYP', tags=['PYP: Юниты. Развитие ATL-навыков']),
    destroy=extend_schema(summary='Удаление пункта развития ATL-навыков в юните PYP', tags=['PYP: Юниты. Развитие ATL-навыков']),
    )
class PypAtlDevelopViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_pyp_atl_develop_queryset()
    filterset_class = PypAtlDevelopFilter
    
    def get_serializer_class(self):
        if self.action == "list":
            return PypAtlDevelopListSerializer
        return PypAtlDevelopUpdateSerializer